# Power Automate Integration Guide - Async API

## 🚨 **Problem Solved: Timeout Issues**

The previous API was timing out because Power Automate has a **5-minute timeout limit**, but our estimation process takes **6-7 minutes**.

## 🔧 **Solution: Async Processing**

### **New API Flow**

#### **Step 1: Submit Job (No Timeout)**
```http
POST /estimate
Content-Type: application/json

{
  "transcript_json": "...",
  "polycam_base64": "..."
}
```

**Response (Immediate):**
```json
{
  "status": "processing",
  "message": "Estimation started in background",
  "job_id": "550e8400-e29b-41d4-a716-446655440000",
  "poll_url": "/estimate_status/550e8400-e29b-41d4-a716-446655440000",
  "estimated_time": "5-7 minutes"
}
```

#### **Step 2: Poll for Results**
```http
GET /estimate_status/550e8400-e29b-41d4-a716-446655440000
```

**Response (While Processing):**
```json
{
  "status": "processing",
  "message": "Job is still processing"
}
```

**Response (When Complete):**
```
[Excel File Download]
Content-Type: application/vnd.openxmlformats-officedocument.spreadsheetml.sheet
Content-Disposition: attachment; filename="comprehensive_clean_estimate_final.xlsx"
```

## 📋 **Power Automate Implementation**

### **1. HTTP Action - Submit Job**
- **Method**: POST
- **URI**: `https://your-ngrok-url.ngrok-free.app/estimate`
- **Headers**: 
  - `Content-Type: application/json`
- **Body**: JSON with transcript and polycam data

### **2. Wait Action**
- **Duration**: 30 seconds (adjust as needed)

### **3. HTTP Action - Check Status**
- **Method**: GET
- **URI**: `https://your-ngrok-url.ngrok-free.app/estimate_status/{job_id}`
- **Headers**: None needed

### **4. Condition Action**
- **If**: `body('Check_Status')?['status'] == 'processing'`
- **Then**: Go back to Wait Action
- **Else**: Continue (file received)

### **5. File Operations**
- **Get file content**: Use the response from the status check
- **Save file**: Store the Excel file in SharePoint/OneDrive

## 🔄 **Complete Flow Example**

```
Power Automate Flow:
├── Submit Job (POST /estimate)
├── Wait 30 seconds
├── Check Status (GET /estimate_status/{job_id})
├── If still processing → Wait 30 seconds → Check Status (loop)
├── If complete → Get file content
└── Save Excel file
```

## ⏱️ **Timing**

- **Job submission**: Immediate response
- **Processing time**: 5-7 minutes (background)
- **Polling interval**: 30 seconds (configurable)
- **Total time**: Same as before, but no timeout errors

## 🎯 **Benefits**

1. ✅ **No more timeouts** - Power Automate gets immediate response
2. ✅ **Reliable file delivery** - File is ready when polling succeeds
3. ✅ **Better error handling** - Clear status updates
4. ✅ **Scalable** - Multiple jobs can run simultaneously
5. ✅ **Power Automate friendly** - Uses standard HTTP patterns

## 🚀 **Ready to Test**

The API is now configured to:
1. **Detect Power Automate requests** automatically
2. **Start background processing** immediately
3. **Return job ID** for tracking
4. **Provide status updates** via polling
5. **Deliver Excel files** when ready

No more timeout errors! 🎉

