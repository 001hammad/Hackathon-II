# Project Libraries and Usage Information

## Frontend Libraries

### Authentication & User Management
- **Better Auth** - Core authentication library
  - Used in: `lib/auth.ts`, `lib/auth-client.ts`, `app/api/auth/[...all]/route.ts`
  - Purpose: Handles user signup, login, sessions, and JWT management

### UI & Styling
- **React** - Core UI library
  - Used throughout: `app/**/*`, `components/**/*`
  - Purpose: Component-based UI rendering

- **Next.js** - React framework
  - Used in: `app/**/*`, `middleware.ts`, `package.json`
  - Purpose: Server-side rendering, routing, and app structure

- **Tailwind CSS** - Styling framework
  - Used in: `globals.css`, `tailwind.config.ts`, `components/**/*`
  - Purpose: Utility-first CSS styling

- **shadcn/ui** - UI component library
  - Used in: `components/ui/**/*`, various components
  - Purpose: Pre-built accessible UI components

- **Framer Motion** - Animation library
  - Used in: Various components with motion effects
  - Purpose: Smooth animations and transitions

### Icons & Graphics
- **Lucide React** - Icon library
  - Used in: Various components for icons
  - Purpose: Consistent icon set

### Type Safety & Utilities
- **TypeScript** - Type checking
  - Used throughout: All `.ts` and `.tsx` files
  - Purpose: Type safety across the application

## Backend Libraries

### Web Framework
- **FastAPI** - Modern Python web framework
  - Used in: `app/main.py`, `app/routes/**/*`, `app/auth/**/*`
  - Purpose: API development with automatic documentation

### Database & ORM
- **SQLModel** - SQL database library
  - Used in: `app/models/**/*`, `app/database/**/*`
  - Purpose: ORM with SQL Alchemy and Pydantic integration

- **SQLAlchemy** - Database toolkit (via SQLModel)
  - Used in: `app/database/**/*`, `app/models/**/*`
  - Purpose: Database operations and connections

- **PostgreSQL (Neon)** - Database system
  - Configured in: `app/database/connection.py`, `app/database/init.py`
  - Purpose: Production database with serverless capabilities

### Authentication & Security
- **python-jose** - JWT handling
  - Used in: `app/core/security.py`, `app/routes/auth.py`
  - Purpose: JWT token creation and verification

- **passlib** - Password hashing (via security module)
  - Used in: `app/core/security.py`
  - Purpose: Secure password hashing

### HTTP & Networking
- **httpx** - HTTP client (likely used by Better Auth)
  - Used by: Better Auth for API calls

### Environment & Configuration
- **python-dotenv** - Environment variable management
  - Used in: `app/core/config.py`, `app/database/connection.py`
  - Purpose: Loading environment variables from .env files

## Development & Build Tools

### Frontend Build Tools
- **ESLint** - Code linting
  - Configured in: `eslint.config.mjs`
  - Purpose: Code quality and consistency

- **PostCSS** - CSS processing
  - Configured in: `postcss.config.mjs`
  - Purpose: CSS transformations

### Package Management
- **npm** - Package manager
  - Used via: `package.json`, `package-lock.json`
  - Purpose: Managing frontend dependencies

- **uv** - Python package manager
  - Used via: `uv.lock`, `pyproject.toml`
  - Purpose: Managing Python dependencies

## Testing & Development
- **pytest** - Testing framework
  - Used in: `tests/**/*`, `app/**/*`
  - Purpose: Unit and integration testing

## Key Integration Points

### Authentication Flow
1. **Better Auth** handles frontend authentication
2. **Next.js BFF** validates sessions and forwards to backend
3. **FastAPI** validates internal headers from BFF

### Database Schema
1. **Better Auth** creates its own user/session tables
2. **SQLModel** creates application-specific tables (users, tasks)
3. **PostgreSQL/Neon** serves as unified database for both

### API Communication
1. **Frontend** makes calls to Next.js API routes
2. **Next.js BFF** validates auth and forwards to FastAPI
3. **FastAPI** processes requests with user context