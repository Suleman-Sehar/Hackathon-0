# 🥉 Bronze Tire Dashboard - Next.js

A sophisticated, modern dashboard for monitoring Bronze Tier AI Employee operations.

![Dashboard Preview](https://img.shields.io/badge/Status-Production%20Ready-success)
![Next.js](https://img.shields.io/badge/Next.js-14-black?logo=next.js)
![TypeScript](https://img.shields.io/badge/TypeScript-5-blue?logo=typescript)
![Tailwind](https://img.shields.io/badge/Tailwind-3-38bdf8?logo=tailwind-css)

---

## ✨ Features

### 🎨 Modern Design
- **Gradient Backgrounds** - Bronze and gold themed gradients
- **Glassmorphism** - Frosted glass header and footer
- **Smooth Animations** - Hover effects and transitions
- **Responsive Layout** - Works on desktop, tablet, and mobile

### 📊 Real-time Data
- **Live Statistics** - Pending/completed tasks, active plans
- **Interactive Charts** - Bar charts and pie charts using Recharts
- **Activity Feed** - Recent completions, emails, WhatsApp messages
- **Directory Monitoring** - Real-time folder status

### 📱 Components
- **Stats Cards** - 4 key metrics with icons and trends
- **Completion Chart** - Tasks completed by plan visualization
- **Priority Distribution** - Pie chart showing P1/P2/P3 breakdown
- **Directory Status** - File counts for each folder
- **Recent Activity** - Timeline of all actions
- **Plans Table** - Detailed view of all plans with status
- **Tags Cloud** - Metadata tags visualization

---

## 🚀 Getting Started

### Prerequisites

- Node.js 18+ installed
- npm or yarn package manager

### Installation

1. **Navigate to the dashboard folder:**
```bash
cd "D:\Hackathon 0\bronze-dashboard"
```

2. **Install dependencies:**
```bash
npm install
```

3. **Run the development server:**
```bash
npm run dev
```

4. **Open your browser:**
Navigate to [http://localhost:3000](http://localhost:3000)

---

## 📁 Project Structure

```
bronze-dashboard/
├── app/
│   ├── api/
│   │   └── dashboard/
│   │       └── route.ts          # API endpoint for dashboard data
│   ├── globals.css               # Global styles
│   ├── layout.tsx                # Root layout
│   └── page.tsx                  # Main dashboard page
├── package.json                  # Dependencies
├── tailwind.config.ts            # Tailwind configuration
├── tsconfig.json                 # TypeScript config
└── next.config.mjs               # Next.js config
```

---

## 🎨 Color Scheme

### Bronze Theme
- **Bronze 500:** `#bfa094` - Primary brand color
- **Bronze 600:** `#a18072` - Hover states
- **Bronze 700:** `#977669` - Active states
- **Bronze 800:** `#846358` - Dark accents

### Gold Theme
- **Gold 400:** `#e8c76e` - Highlights
- **Gold 500:** `#d9a32e` - Primary gold
- **Gold 600:** `#cf8b1f` - Hover states
- **Gold 700:** `#ad6f19` - Dark gold

---

## 📊 Dashboard Sections

### 1. Header
- Logo and title
- Last updated timestamp
- Live status indicator

### 2. Success Banner
- Shows when all tasks are completed
- Displays achievement message
- Animated celebration elements

### 3. Stats Cards
- **Pending Tasks** - Amber themed
- **Completed Tasks** - Emerald themed
- **Active Plans** - Blue themed
- **Completed Plans** - Gold themed

### 4. Charts
- **Tasks Completed by Plan** - Bar chart
- **Priority Distribution** - Pie chart

### 5. Directory Status
- Inbox
- Needs_Action
- Plans
- Done
- Logs

### 6. Recent Activity
- Task completions
- Email sent
- WhatsApp messages
- LinkedIn posts

### 7. Plans Table
- Plan name
- Priority (P1/P2/P3)
- Task count
- Due date
- Status

### 8. Metadata Tags
- Hashtag styled tags
- Total files tracked
- System status

---

## 🔧 Customization

### Update Colors

Edit `tailwind.config.ts`:

```typescript
colors: {
  bronze: {
    // Your custom bronze colors
  },
  gold: {
    // Your custom gold colors
  },
}
```

### Add New Metrics

Edit `app/page.tsx` and add to `statsCards` array:

```typescript
{
  title: 'New Metric',
  value: data.newMetric,
  icon: YourIcon,
  color: 'text-custom-600',
  bgColor: 'bg-custom-50',
  trend: 'positive',
}
```

---

## 📦 Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| next | 14.1.0 | React framework |
| react | 18.2.0 | UI library |
| recharts | 2.10.4 | Charts |
| lucide-react | 0.321.0 | Icons |
| tailwindcss | 3.4.1 | Styling |
| typescript | 5.3.3 | Type safety |

---

## 🛠️ Development

### Build for Production

```bash
npm run build
npm start
```

### Linting

```bash
npm run lint
```

### Type Checking

```bash
npx tsc --noEmit
```

---

## 🌐 Deployment

### Vercel (Recommended)

1. Push code to GitHub
2. Import project in Vercel
3. Deploy automatically

### Docker

```bash
docker build -t bronze-dashboard .
docker run -p 3000:3000 bronze-dashboard
```

---

## 📸 Screenshots

### Desktop View
- Full dashboard with all components
- Responsive grid layout
- Interactive charts

### Mobile View
- Stacked cards
- Touch-friendly buttons
- Optimized charts

---

## 🔐 Security

- No sensitive data exposed
- API endpoint reads from local files only
- No external API calls
- Client-side rendering

---

## 📝 License

MIT License - Feel free to use in your projects!

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

---

## 📞 Support

For issues or questions:
- Check the documentation
- Review existing issues
- Create a new issue

---

## 🎯 Future Enhancements

- [ ] Real-time WebSocket updates
- [ ] Dark mode toggle
- [ ] Export to PDF/CSV
- [ ] Custom date range filtering
- [ ] Email notifications
- [ ] Mobile app version
- [ ] Multi-tier comparison view
- [ ] Historical data charts

---

**Built with ❤️ by Suleman AI Employee**

*Bronze Tier Dashboard - Production Ready*
