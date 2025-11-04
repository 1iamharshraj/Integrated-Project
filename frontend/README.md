# ZeTheta FinArcade - Frontend

India's first fully autonomous AI-driven investment advisory platform - Next.js Frontend Application.

## 🚀 Features

- **Complete API Integration**: All backend endpoints integrated
- **Authentication**: Secure login/register with JWT tokens
- **Portfolio Management**: View and manage investment portfolio
- **Risk Profiling**: Comprehensive risk assessment with Q-Score, G-Score, B-Score
- **Goals Management**: Track financial goals with Monte Carlo simulations
- **Market Data**: Real-time market indices, sentiment, and predictions
- **AI Insights**: AI-powered recommendations and insights
- **Behavioral Analytics**: Track investment behavior
- **KYC Management**: Document upload and verification
- **Transactions**: Complete transaction history
- **Education**: Financial education resources
- **Dark Mode**: Full theme support

## 📁 Project Structure

```
frontend/
├── src/
│   ├── app/                    # Next.js app router pages
│   │   ├── (auth)/             # Authentication pages
│   │   ├── (dashboard)/        # Dashboard pages (protected)
│   │   ├── onboarding/        # Onboarding wizard
│   │   ├── layout.tsx          # Root layout
│   │   └── page.tsx            # Home page
│   ├── components/
│   │   ├── ui/                 # shadcn/ui components
│   │   ├── layout/             # Layout components
│   │   ├── portfolio/          # Portfolio components
│   │   ├── risk-profiling/     # Risk profiling components
│   │   ├── goals/              # Goals components
│   │   ├── market/             # Market components
│   │   ├── ai-insights/        # AI insights components
│   │   ├── behavioral/        # Behavioral components
│   │   ├── kyc/                # KYC components
│   │   ├── transactions/       # Transaction components
│   │   └── education/          # Education components
│   ├── lib/
│   │   ├── api/                # API client modules
│   │   ├── utils/              # Utility functions
│   │   └── hooks/              # Custom React hooks
│   ├── store/                  # Zustand stores
│   ├── types/                  # TypeScript type definitions
│   └── styles/
│       └── globals.css          # Global styles
├── public/                     # Static assets
├── .env.local                  # Environment variables
└── package.json

```

## 🛠️ Tech Stack

- **Next.js 14+** (App Router)
- **TypeScript**
- **Tailwind CSS** (with custom design system)
- **shadcn/ui** (Component library)
- **Zustand** (State management)
- **React Query** (Data fetching)
- **React Hook Form** + **Zod** (Form validation)
- **Axios** (HTTP client)
- **Recharts** (Data visualization)
- **Framer Motion** (Animations)
- **Lucide React** (Icons)

## 📦 Installation

1. **Install dependencies**:
   ```bash
   npm install
   ```

2. **Set up environment variables**:
   Create `.env.local`:
   ```env
   NEXT_PUBLIC_API_URL=http://localhost:5000/api
   NEXT_PUBLIC_APP_NAME=ZeTheta FinArcade
   ```

3. **Run development server**:
   ```bash
   npm run dev
   ```

4. **Build for production**:
   ```bash
   npm run build
   ```

## 🔌 API Integration

All API endpoints are integrated in `src/lib/api/`:

- `auth.ts` - Authentication endpoints
- `portfolio.ts` - Portfolio management
- `risk-profiling.ts` - Risk profiling
- `goals.ts` - Goals management
- `market.ts` - Market data
- `ai-insights.ts` - AI insights
- `behavioral.ts` - Behavioral analytics
- `kyc.ts` - KYC documents
- `transactions.ts` - Transactions
- `education.ts` - Education progress
- `news.ts` - News and sentiment

## 🎨 Design System

The application uses a comprehensive design system matching Project 25:

- **Colors**: CSS variables for theming
- **Typography**: Inter font family
- **Components**: shadcn/ui with custom styling
- **Animations**: Framer Motion for smooth transitions
- **Responsive**: Mobile-first design

## 📱 Pages

### Public Pages
- `/` - Home page with hero, features, pricing
- `/login` - User login
- `/register` - User registration

### Protected Pages (Dashboard)
- `/dashboard` - Main dashboard
- `/portfolio` - Portfolio management
- `/risk-profiling` - Risk assessment
- `/goals` - Financial goals
- `/market` - Market data
- `/ai-insights` - AI recommendations
- `/behavioral` - Behavioral analytics
- `/transactions` - Transaction history
- `/kyc` - KYC documents
- `/education` - Education resources
- `/settings` - Account settings

## 🔐 Authentication

- JWT-based authentication
- Token refresh mechanism
- Protected routes with middleware
- Persistent authentication state

## 🎯 State Management

- **Auth Store**: User authentication and profile
- **Portfolio Store**: Portfolio data and holdings
- **UI Store**: Theme and UI preferences

## 📝 TypeScript

All components and utilities are fully typed with comprehensive TypeScript definitions in `src/types/`.

## 🚧 Development Status

### ✅ Completed
- Project setup and configuration
- API client and all API modules
- Type definitions
- Zustand stores
- Essential UI components
- Layout components (Navigation, Sidebar, Header, Footer)
- Authentication pages
- Home page
- Dashboard layout and main dashboard
- Basic page structure for all routes

### 🔄 In Progress / To Be Completed
- Onboarding wizard (multi-step)
- Portfolio components (charts, tables)
- Risk profiling forms and visualizations
- Goals components with Monte Carlo
- Market data components
- AI insights components
- Behavioral analytics components
- KYC upload components
- Transaction management
- Education components
- Settings page

## 📚 Documentation

- API endpoints are documented in the backend
- Component props are typed with TypeScript
- Code follows Next.js 14+ best practices

## 🤝 Contributing

This is a complete frontend application structure. Individual components and pages can be enhanced and expanded as needed.

## 📄 License

Proprietary - ZeTheta FinArcade
