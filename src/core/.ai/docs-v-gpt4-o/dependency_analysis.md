# Dependency Analysis

## Internal Dependencies Map
The project follows a modular monolithic architecture with distinct layers and components:
1. **Configuration Layer (`_0_config`)**:
   - Centralized settings split into multiple files (e.g., `DATABASE_CONFIG.py`, `AUTH_AND_SESSION_CONFIG.py`).
   - Entry points for WSGI/ASGI and URL routing (`asgi.py`, `wsgi.py`, `urls.py`).

2. **Shared Kernel (`___utils`)**:
   - Provides reusable utilities, base models, middleware, and services.
   - Sub-components:
     - `functions/`: Utility functions for data manipulation (e.g., `json_function.py`, `string_function.py`).
     - `models/`: Abstract base models (`basic_model.py`) with common fields like timestamps and soft-delete logic.
     - `service/`: External integrations (e.g., `crypto_service.py`, `email_service.py`, `payment/zarinpal_service.py`).
     - `middlewares/`: Request processing hooks (e.g., `access_middleware.py`, `ip_address_middleware.py`).

3. **Core Domain Layer (`_2_account`, `_1_site_setting`)**:
   - Handles user management and site configuration.
   - Modularized into sub-components (`_modules/register_user`, `_modules/user_setting`).

4. **Business Domain Layer (`apps`)**:
   - Contains business logic modules such as `category` and `social_network`.

5. **Presentation Layer (`_2_panel_admin`, `_2_panel_user`, `ztemplates`)**:
   - Admin and user dashboards with decoupled UI logic.

## External Libraries Analysis
### Core Dependencies
- **Django Framework**:
  - `django==5.2.8`: Core web framework.
  - `django-cleanup==9.0.0`: Automatic cleanup of files for models.
  - `django-jalali-date==2.0.0`: Jalali date support.
  - `django-multiselectfield==1.0.1`: Multi-select field for models.
  - `django-render-partial==0.4`: Partial template rendering.
  - `django-simple-history==3.10.1`: Historical tracking for models.
  - `django-translated-fields==0.13.0`: Multi-language field support.

- **Database**:
  - `psycopg==3.2.12`: PostgreSQL database adapter.
  - `sqlparse==0.5.3`: SQL parsing library.

- **Utilities**:
  - `python-dateutil==2.9.0.post0`: Date and time manipulation.
  - `python-decouple==3.8`: Environment variable management.
  - `pytz==2025.2`: Timezone support.
  - `regex==2025.11.3`: Regular expressions.
  - `unidecode==0.4.21`: Unicode string normalization.

- **Media**:
  - `pillow==12.0.0`: Image processing.
  - `sorl-thumbnail==12.11.0`: Thumbnail generation.

- **CKEditor**:
  - `django-ckeditor-5==0.2.18`: Rich text editor integration.

- **HTMX**:
  - `django-htmx==1.26.0`: HTML-over-the-wire framework.

### Optional Dependencies
- **Blockchain**:
  - `solana==0.36.9`, `tronpy==0.6.1`, `blockcypher==1.0.93`: Blockchain integrations.
  - `websockets==15.0.1`: WebSocket support for blockchain interactions.

- **GIS**:
  - `geopy==2.4.1`, `reverse-geocoder==1.5.1`: Geospatial data processing.

- **Authentication**:
  - `django-allauth==65.10.0`: Social authentication.
  - `PyJWT==2.10.1`: JSON Web Token support.

- **Others**:
  - `gunicorn==23.0.0`: WSGI HTTP server for Python web applications.

## Service Integrations
1. **Crypto Services**:
   - Blockchain interactions (e.g., Solana, Tron, BlockCypher).
   - Sub-services for smart contracts, address validation, and RPC calls.

2. **Payment Gateway**:
   - `zarinpal_service.py`: Integration with Zarinpal payment provider.

3. **Communication Services**:
   - `email_service.py`: Email sending with template support.
   - `sms_service.py`: SMS provider integration.

4. **GIS Services**:
   - Geospatial data processing using libraries like `geopy` and `reverse-geocoder`.

5. **Authentication**:
   - Social authentication via `django-allauth`.

## Dependency Injection Patterns
- **Service Layer**:
  - Services are centralized in `___utils/service` and injected into components as needed.
  - Example: `crypto_service.py` orchestrates blockchain operations using utility scripts.

- **Base Classes**:
  - `basic_model.py` and `base_view.py` act as layer supertypes, providing shared functionality.

- **Configuration Injection**:
  - Settings are imported from `_0_config/configs` into `settings.py`.

## Module Coupling Assessment
- **High Coupling**:
  - `_0_config` is tightly coupled with all components due to its role in managing settings.
  - `___utils` is heavily relied upon by `apps` and `_2_account`.

- **Moderate Coupling**:
  - `apps` and `_2_account` interact with `___utils` for shared services and models.

- **Low Coupling**:
  - `ztemplates` and `_2_panel_admin` are decoupled from the data models, focusing solely on presentation.

## Dependency Graph
```
_0_config
  ├── ___utils
  │     ├── functions
  │     ├── models
  │     ├── service
  │     ├── middlewares
  │     └── views
  ├── _2_account
  │     ├── _modules/register_user
  │     ├── _modules/user_setting
  │     └── _modules/user_social_media
  ├── _1_site_setting
  │     ├── _modules/footer
  │     ├── _modules/header
  │     └── _modules/site_social_media
  ├── apps
  │     ├── category
  │     └── social_network
  ├── _2_panel_admin
  ├── _2_panel_user
  └── ztemplates
```

## Potential Dependency Issues
1. **Tight Coupling**:
   - `_0_config` is a single point of failure. Any changes here could impact all components.
   - `___utils` is heavily relied upon, which may lead to challenges in testing and modularization.

2. **Circular Dependencies**:
   - Potential circular dependencies between `___utils/service` and its sub-components (e.g., `crypto/utils`).

3. **Unused Dependencies**:
   - Several libraries in `development.txt` and `production.txt` are commented out, indicating potential redundancy or incomplete integrations.

4. **Version Management**:
   - Some libraries (e.g., `django`, `pillow`) are pinned to specific versions, which may cause compatibility issues during upgrades.

5. **Service Overlap**:
   - Multiple services for similar functionalities (e.g., `crypto_service.py` and `crypto/utils`) may lead to redundancy.

6. **Documentation Gaps**:
   - While some components have documentation, others lack detailed explanations (e.g., `___utils/functions`).

## Recommendations
1. **Decouple Configuration**:
   - Consider modularizing `_0_config` further to reduce coupling.

2. **Refactor Utility Layer**:
   - Evaluate `___utils` for redundant or overly complex components.

3. **Dependency Cleanup**:
   - Remove unused or commented-out dependencies from `development.txt` and `production.txt`.

4. **Version Updates**:
   - Regularly update dependencies to avoid security vulnerabilities.

5. **Improve Documentation**:
   - Expand documentation for under-documented components.

6. **Dependency Injection Framework**:
   - Consider using a DI framework to manage service dependencies more effectively.