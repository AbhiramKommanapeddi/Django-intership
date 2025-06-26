# Django Internship Assignment - API Logging System

## Complete Example of API Log Tracking

### What is API Logging?

API logging is the process of automatically recording information about every HTTP request made to your API endpoints. This is crucial for:

- **Monitoring**: Track API usage and performance
- **Security**: Detect suspicious activities and unauthorized access attempts
- **Debugging**: Identify issues and bottlenecks
- **Analytics**: Understand user behavior and popular endpoints
- **Compliance**: Maintain audit trails for regulatory requirements

### API Log Fields Explained

#### 1. **Endpoint**

- **Description**: The URL path that was accessed
- **Example**: `/api/protected/`, `/api/login/`, `/api/public/`
- **Purpose**: Identify which functionality was used

#### 2. **Method**

- **Description**: HTTP method used for the request
- **Examples**: `GET`, `POST`, `PUT`, `DELETE`, `PATCH`
- **Purpose**: Understand the type of operation performed

#### 3. **User**

- **Description**: The authenticated user who made the request
- **Examples**: `admin`, `testuser`, `Anonymous` (for unauthenticated requests)
- **Purpose**: Track who is using your API

#### 4. **IP Address**

- **Description**: The client's IP address
- **Examples**: `127.0.0.1`, `192.168.1.100`, `203.0.113.45`
- **Purpose**: Identify the source of requests, detect suspicious patterns

#### 5. **Response Status**

- **Description**: HTTP status code returned by the server
- **Examples**:
  - `200` (OK) - Successful request
  - `201` (Created) - Resource created successfully
  - `400` (Bad Request) - Client error
  - `401` (Unauthorized) - Authentication required
  - `403` (Forbidden) - Access denied
  - `404` (Not Found) - Resource not found
  - `500` (Internal Server Error) - Server error
- **Purpose**: Track success/failure rates and identify issues

#### 6. **Response Time**

- **Description**: Time taken to process the request (in seconds)
- **Examples**: `0.045` (45ms), `0.234` (234ms), `1.250` (1.25s)
- **Purpose**: Monitor API performance and identify slow endpoints

#### 7. **Timestamp**

- **Description**: When the request was made
- **Example**: `2025-06-26 09:30:15.123456+00:00`
- **Purpose**: Track usage patterns over time

---

## Real Examples from Django Internship Project

### Example 1: Successful Public API Access

```
Endpoint: /api/public/
Method: GET
User: Anonymous
IP Address: 127.0.0.1
Response Status: 200 (OK)
Response Time: 0.045 seconds
Timestamp: 2025-06-26 09:30:15+00:00
```

**Analysis**: Anonymous user successfully accessed public endpoint quickly (45ms).

### Example 2: Unauthorized Access Attempt

```
Endpoint: /api/protected/
Method: GET
User: Anonymous
IP Address: 192.168.1.102
Response Status: 401 (Unauthorized)
Response Time: 0.012 seconds
Timestamp: 2025-06-26 09:30:20+00:00
```

**Analysis**: Someone tried to access protected content without authentication. Fast rejection (12ms).

### Example 3: Successful Authenticated Access

```
Endpoint: /api/protected/
Method: GET
User: admin
IP Address: 127.0.0.1
Response Status: 200 (OK)
Response Time: 0.123 seconds
Timestamp: 2025-06-26 09:30:25+00:00
```

**Analysis**: Admin user successfully accessed protected endpoint. Slightly slower due to authentication checks.

### Example 4: Failed Registration Attempt

```
Endpoint: /api/register/
Method: POST
User: Anonymous
IP Address: 192.168.1.103
Response Status: 400 (Bad Request)
Response Time: 0.156 seconds
Timestamp: 2025-06-26 09:30:30+00:00
```

**Analysis**: Registration failed due to invalid data (e.g., username already exists).

---

## Django Admin Interface Features

### ChangeAddDeleteView Functionality

The Django admin provides a powerful interface for managing API logs:

#### **Change View** (Read-Only)

- View individual log entries with all details
- Organized in fieldsets for better readability
- Cannot modify logs (data integrity)

#### **Add View** (Disabled)

- Add functionality is disabled for logs
- Logs are created automatically by the system
- Prevents manual log creation that could compromise data

#### **Delete View** (Restricted)

- Only superusers can delete logs
- Bulk delete operations available
- Confirmation required for deletions

#### **List View Features**

- **Filtering**: Filter by method, status code, date, user
- **Searching**: Search by endpoint, username, IP address
- **Sorting**: Sort by any column (timestamp, response time, etc.)
- **Pagination**: 25 logs per page for performance
- **Color Coding**:
  - Green: Successful requests (200, 201)
  - Orange: Client errors (400, 404)
  - Red: Authentication/Server errors (401, 403, 500)

---

## Access the API Logs

### Via Django Admin

1. Navigate to: http://localhost:8000/admin/
2. Login with: username=`admin`, password=`admin123`
3. Go to: **Home › Api › Api logs**
4. Explore the comprehensive logging interface

### Via API Endpoint

- **URL**: `GET /api/logs/`
- **Authentication**: Required (admin users only)
- **Response**: JSON array of recent API logs

---

## Benefits of This Logging System

### 1. **Security Monitoring**

- Track failed authentication attempts
- Identify suspicious IP addresses
- Monitor access patterns

### 2. **Performance Analysis**

- Identify slow endpoints
- Monitor response times
- Track usage patterns

### 3. **Usage Analytics**

- Most popular endpoints
- User activity patterns
- Peak usage times

### 4. **Debugging Support**

- Trace request flow
- Identify error patterns
- Correlate issues with timing

### 5. **Compliance & Auditing**

- Complete audit trail
- Data access logging
- Regulatory compliance support

---

## Production Considerations

### Storage

- Implement log rotation to manage disk space
- Consider archiving old logs to cold storage
- Use database indexes for query performance

### Privacy

- Be mindful of logging sensitive data
- Consider IP anonymization for GDPR compliance
- Implement data retention policies

### Performance

- Use background tasks for heavy log processing
- Implement sampling for high-traffic APIs
- Monitor logging overhead

This comprehensive API logging system provides enterprise-level monitoring and debugging capabilities for the Django Internship Assignment project.
