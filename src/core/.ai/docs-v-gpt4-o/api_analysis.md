# API Documentation

## APIs Served by This Project

### Endpoints

#### 1. CKEditor File Upload
- **Method and Path**: `GET /ckeditor5/`
- **Description**: Endpoint for handling file uploads via CKEditor 5.
- **Request**:
  - **Headers**: None specified.
  - **Params**: None specified.
  - **Body**: None specified.
- **Response**:
  - **Success**: File upload confirmation.
  - **Error**: Error message indicating upload failure.
- **Authentication**: None specified.
- **Examples**:
  ```bash
  curl -X GET http://<base_url>/ckeditor5/
  ```

#### 2. Authentication
- **Method and Path**: `GET /auth/`
- **Description**: Authentication-related endpoints, including login, registration, and password reset.
- **Request**:
  - **Headers**: None specified.
  - **Params**: None specified.
  - **Body**: None specified.
- **Response**:
  - **Success**: Authentication success message or user data.
  - **Error**: Error message indicating authentication failure.
- **Authentication**: Required for certain endpoints.
- **Examples**:
  ```bash
  curl -X GET http://<base_url>/auth/
  ```

#### 3. Admin Panel
- **Method and Path**: `GET /panel-admin/`
- **Description**: Custom admin panel for managing the application.
- **Request**:
  - **Headers**: None specified.
  - **Params**: None specified.
  - **Body**: None specified.
- **Response**:
  - **Success**: Admin panel interface.
  - **Error**: Error message indicating access issues.
- **Authentication**: Required.
- **Examples**:
  ```bash
  curl -X GET http://<base_url>/panel-admin/
  ```

#### 4. User Panel
- **Method and Path**: `GET /user/`
- **Description**: User panel for managing user-specific settings and data.
- **Request**:
  - **Headers**: None specified.
  - **Params**: None specified.
  - **Body**: None specified.
- **Response**:
  - **Success**: User panel interface.
  - **Error**: Error message indicating access issues.
- **Authentication**: Required.
- **Examples**:
  ```bash
  curl -X GET http://<base_url>/user/
  ```

#### 5. Faker Data
- **Method and Path**: `GET /faker/`
- **Description**: Endpoint for generating fake data for testing purposes.
- **Request**:
  - **Headers**: None specified.
  - **Params**: None specified.
  - **Body**: None specified.
- **Response**:
  - **Success**: Generated fake data.
  - **Error**: Error message indicating generation failure.
- **Authentication**: None specified.
- **Examples**:
  ```bash
  curl -X GET http://<base_url>/faker/
  ```

#### 6. User Settings
- **Method and Path**: `GET /set-user-setting/`
- **Description**: Endpoint for managing user-specific settings.
- **Request**:
  - **Headers**: None specified.
  - **Params**: None specified.
  - **Body**: None specified.
- **Response**:
  - **Success**: User settings data.
  - **Error**: Error message indicating access issues.
- **Authentication**: Required.
- **Examples**:
  ```bash
  curl -X GET http://<base_url>/set-user-setting/
  ```

#### 7. Site Settings
- **Method and Path**: `GET /`
- **Description**: Endpoint for managing site-wide settings.
- **Request**:
  - **Headers**: None specified.
  - **Params**: None specified.
  - **Body**: None specified.
- **Response**:
  - **Success**: Site settings data.
  - **Error**: Error message indicating access issues.
- **Authentication**: None specified.
- **Examples**:
  ```bash
  curl -X GET http://<base_url>/
  ```

### Authentication & Security
- **Authentication Methods**:
  - Custom authentication endpoints (`/auth/`).
  - Integration with Django Allauth (`/accounts/`).
- **Security Considerations**:
  - Middleware for access control and IP address validation.
  - Session and cookie management for secure user authentication.
  - Use of QR codes for two-factor authentication.

### Rate Limiting & Constraints
- No explicit rate-limiting mechanisms were identified in the codebase. Developers should consider implementing rate-limiting middleware or using third-party services like Django Ratelimit.

## External API Dependencies

### Services Consumed

#### 1. Zarinpal Payment Gateway
- **Service Name & Purpose**: Zarinpal Service for payment processing.
- **Base URL/Configuration**: Defined in `___utils/service/payment/zarinpal/zarinpal_variable.py`.
- **Endpoints Used**: Payment initiation, verification, and refund.
- **Authentication Method**: API keys configured in environment variables.
- **Error Handling**: Custom error messages for payment failures.
- **Retry/Circuit Breaker Configuration**: Not explicitly implemented; consider adding retry logic for network failures.

#### 2. Blockchain Services
- **Service Name & Purpose**: Crypto Service for blockchain interactions.
- **Base URL/Configuration**: RPC URLs defined in `___utils/service/crypto/utils/public_rpc_finder.py`.
- **Endpoints Used**: Wallet creation, balance check, transaction signing.
- **Authentication Method**: API keys or tokens for blockchain providers.
- **Error Handling**: Error messages for invalid transactions or network issues.
- **Retry/Circuit Breaker Configuration**: Not explicitly implemented; consider adding retry logic for network failures.

#### 3. Email Service
- **Service Name & Purpose**: Email Service for sending transactional emails.
- **Base URL/Configuration**: SMTP server details defined in `_0_config/configs/EMAIL_CONFIG.py`.
- **Endpoints Used**: Email sending.
- **Authentication Method**: SMTP credentials.
- **Error Handling**: Retry logic for failed email sends.
- **Retry/Circuit Breaker Configuration**: Not explicitly implemented; consider adding retry logic for network failures.

#### 4. SMS Service
- **Service Name & Purpose**: SMS Service for sending text messages.
- **Base URL/Configuration**: Provider details defined in `___utils/service/sms_service.py`.
- **Endpoints Used**: SMS sending.
- **Authentication Method**: API keys configured in environment variables.
- **Error Handling**: Custom error messages for SMS failures.
- **Retry/Circuit Breaker Configuration**: Not explicitly implemented; consider adding retry logic for network failures.

### Integration Patterns
- **Service Layer**: External integrations are abstracted into service classes within `___utils/service`.
- **Configuration Management**: Environment variables are used for dynamic configuration of external services.
- **Error Handling**: Custom error messages are implemented for various services, but retry logic and circuit breakers are not explicitly defined.

## Available Documentation
- **Root Help Files**:
  - `/#help_database.txt`: Database setup/maintenance instructions.
  - `/#help_git.txt`: Git workflow guidelines.
  - `/#help_translate_django.txt`: Guide for the i18n/translation workflow.
- **Service Documentation**:
  - `___utils/service/crypto/_help_en.txt` & `_help_fa.txt`: Bilingual documentation for the crypto service.
- **Middleware Documentation**:
  - `___utils/middlewares/__docs.py`: Explains middleware pipeline order and responsibility.

**Quality Evaluation**:
The documentation is developer-centric and operational, with bilingual help files indicating a multi-lingual team or target audience. The `__docs.py` pattern is unconventional but useful for keeping documentation close to the code.