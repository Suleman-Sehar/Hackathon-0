'use client';

import { useEffect, useState } from 'react';
import { 
  CheckCircle, 
  Clock, 
  FileText, 
  Folder, 
  TrendingUp,
  Activity,
  Mail,
  MessageCircle,
  Linkedin,
  Award,
  Calendar,
  BarChart3,
  PieChart
} from 'lucide-react';
import { 
  BarChart, 
  Bar, 
  XAxis, 
  YAxis, 
  CartesianGrid, 
  Tooltip, 
  ResponsiveContainer,
  PieChart as RechartsPieChart,
  Pie,
  Cell
} from 'recharts';

interface DashboardData {
  lastUpdated: string;
  quickStats: {
    pendingTasks: number;
    completedTasks: number;
    activePlans: number;
    completedPlans: number;
  };
  directoryStatus: {
    name: string;
    count: number;
    status: 'ok' | 'warning' | 'empty';
  }[];
  completionReports: {
    title: string;
    date: string;
    tasksCompleted: number;
  }[];
  recentActivity: {
    action: string;
    description: string;
    timestamp: string;
    type: 'completion' | 'email' | 'whatsapp' | 'linkedin';
  }[];
  plans: {
    name: string;
    priority: 'P1' | 'P2' | 'P3';
    tasks: number;
    due: string | null;
    status: 'completed' | 'active' | 'overdue';
  }[];
  metadata: {
    totalFilesTracked: number;
    tags: string[];
  };
}

const COLORS = ['#bfa094', '#d9a32e', '#6f5248', '#a18072', '#e8c76e'];

export default function Dashboard() {
  const [data, setData] = useState<DashboardData | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch('/api/dashboard')
      .then((res) => res.json())
      .then((data) => {
        setData(data);
        setLoading(false);
      })
      .catch((err) => {
        console.error(err);
        setLoading(false);
      });
  }, []);

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-bronze-50 via-white to-gold-50 flex items-center justify-center">
        <div className="text-center">
          <div className="w-16 h-16 border-4 border-bronze-500 border-t-transparent rounded-full animate-spin mx-auto mb-4"></div>
          <p className="text-bronze-800 text-lg font-medium">Loading Dashboard...</p>
        </div>
      </div>
    );
  }

  if (!data) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-bronze-50 via-white to-gold-50 flex items-center justify-center">
        <div className="text-center text-bronze-800">
          <p className="text-lg font-medium">Failed to load dashboard data</p>
        </div>
      </div>
    );
  }

  const statsCards = [
    {
      title: 'Pending Tasks',
      value: data.quickStats.pendingTasks,
      icon: Clock,
      color: 'text-amber-600',
      bgColor: 'bg-amber-50',
      trend: data.quickStats.pendingTasks === 0 ? 'positive' : 'neutral',
    },
    {
      title: 'Completed Tasks',
      value: data.quickStats.completedTasks,
      icon: CheckCircle,
      color: 'text-emerald-600',
      bgColor: 'bg-emerald-50',
      trend: 'positive',
    },
    {
      title: 'Active Plans',
      value: data.quickStats.activePlans,
      icon: FileText,
      color: 'text-blue-600',
      bgColor: 'bg-blue-50',
      trend: 'neutral',
    },
    {
      title: 'Completed Plans',
      value: data.quickStats.completedPlans,
      icon: Award,
      color: 'text-gold-600',
      bgColor: 'bg-gold-50',
      trend: 'positive',
    },
  ];

  const priorityData = [
    { name: 'P1', value: 0, color: '#ef4444' },
    { name: 'P2', value: 0, color: '#f59e0b' },
    { name: 'P3', value: 0, color: '#10b981' },
  ];

  const completionData = data.completionReports.map(report => ({
    name: report.title.replace('COMPLETION_', '').replace(/_/g, ' '),
    tasks: report.tasksCompleted,
  }));

  return (
    <div className="min-h-screen bg-gradient-to-br from-bronze-50 via-white to-gold-50">
      {/* Header */}
      <header className="bg-white/80 backdrop-blur-md border-b border-bronze-200 sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center py-4">
            <div className="flex items-center space-x-3">
              <div className="w-12 h-12 bg-gradient-to-br from-bronze-500 to-bronze-700 rounded-xl flex items-center justify-center shadow-lg">
                <Award className="w-7 h-7 text-white" />
              </div>
              <div>
                <h1 className="text-2xl font-bold bg-gradient-to-r from-bronze-600 to-gold-600 bg-clip-text text-transparent">
                  Bronze Tire Dashboard
                </h1>
                <p className="text-sm text-gray-500">AI Employee Operations Center</p>
              </div>
            </div>
            <div className="flex items-center space-x-4">
              <div className="text-right">
                <p className="text-xs text-gray-500">Last Updated</p>
                <p className="text-sm font-medium text-bronze-800">{data.lastUpdated}</p>
              </div>
              <div className="w-3 h-3 bg-emerald-500 rounded-full animate-pulse"></div>
            </div>
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Success Banner */}
        {data.quickStats.pendingTasks === 0 && (
          <div className="mb-8 bg-gradient-to-r from-emerald-500 to-emerald-600 rounded-2xl p-6 text-white shadow-xl">
            <div className="flex items-center justify-between">
              <div className="flex items-center space-x-4">
                <div className="w-12 h-12 bg-white/20 rounded-full flex items-center justify-center">
                  <CheckCircle className="w-7 h-7" />
                </div>
                <div>
                  <h2 className="text-xl font-bold">All Tasks Completed! 🎉</h2>
                  <p className="text-emerald-100">Inbox Zero achieved - All {data.quickStats.completedTasks} tasks completed</p>
                </div>
              </div>
              <Award className="w-16 h-16 text-white/30" />
            </div>
          </div>
        )}

        {/* Stats Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          {statsCards.map((stat) => (
            <div
              key={stat.title}
              className="bg-white rounded-2xl p-6 shadow-lg hover:shadow-xl transition-all duration-300 border border-gray-100"
            >
              <div className="flex items-center justify-between mb-4">
                <div className={`w-12 h-12 ${stat.bgColor} rounded-xl flex items-center justify-center`}>
                  <stat.icon className={`w-6 h-6 ${stat.color}`} />
                </div>
                {stat.trend === 'positive' && (
                  <TrendingUp className="w-5 h-5 text-emerald-500" />
                )}
              </div>
              <p className="text-gray-500 text-sm font-medium mb-1">{stat.title}</p>
              <p className="text-4xl font-bold text-gray-900">{stat.value}</p>
            </div>
          ))}
        </div>

        {/* Charts Row */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
          {/* Completion Reports Chart */}
          <div className="bg-white rounded-2xl p-6 shadow-lg border border-gray-100">
            <div className="flex items-center justify-between mb-6">
              <div className="flex items-center space-x-3">
                <BarChart3 className="w-6 h-6 text-bronze-600" />
                <h3 className="text-lg font-bold text-gray-900">Tasks Completed by Plan</h3>
              </div>
            </div>
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={completionData}>
                <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
                <XAxis dataKey="name" stroke="#9ca3af" fontSize={12} />
                <YAxis stroke="#9ca3af" fontSize={12} />
                <Tooltip
                  contentStyle={{
                    backgroundColor: 'white',
                    border: '1px solid #e5e7eb',
                    borderRadius: '8px',
                  }}
                />
                <Bar dataKey="tasks" fill="url!(colorBronze)" radius={[8, 8, 0, 0]} />
                <defs>
                  <linearGradient id="colorBronze" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#bfa094" stopOpacity={0.8} />
                    <stop offset="95%" stopColor="#bfa094" stopOpacity={1} />
                  </linearGradient>
                </defs>
              </BarChart>
            </ResponsiveContainer>
          </div>

          {/* Priority Distribution */}
          <div className="bg-white rounded-2xl p-6 shadow-lg border border-gray-100">
            <div className="flex items-center justify-between mb-6">
              <div className="flex items-center space-x-3">
                <PieChart className="w-6 h-6 text-gold-600" />
                <h3 className="text-lg font-bold text-gray-900">Priority Distribution</h3>
              </div>
            </div>
            <ResponsiveContainer width="100%" height={300}>
              <RechartsPieChart>
                <Pie
                  data={priorityData}
                  cx="50%"
                  cy="50%"
                  labelLine={false}
                  label={({ name, percent }) => `${name}: ${(percent * 100).toFixed(0)}%`}
                  outerRadius={100}
                  fill="#8884d8"
                  dataKey="value"
                >
                  {priorityData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={entry.color} />
                  ))}
                </Pie>
                <Tooltip />
              </RechartsPieChart>
            </ResponsiveContainer>
            <div className="flex justify-center space-x-6 mt-4">
              {priorityData.map((item) => (
                <div key={item.name} className="flex items-center space-x-2">
                  <div
                    className="w-3 h-3 rounded-full"
                    style={{ backgroundColor: item.color }}
                  ></div>
                  <span className="text-sm text-gray-600">{item.name}</span>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Directory Status & Recent Activity */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-8">
          {/* Directory Status */}
          <div className="lg:col-span-1 bg-white rounded-2xl p-6 shadow-lg border border-gray-100">
            <div className="flex items-center space-x-3 mb-6">
              <Folder className="w-6 h-6 text-bronze-600" />
              <h3 className="text-lg font-bold text-gray-900">Directory Status</h3>
            </div>
            <div className="space-y-3">
              {data.directoryStatus.map((dir) => (
                <div
                  key={dir.name}
                  className="flex items-center justify-between p-3 bg-gray-50 rounded-xl"
                >
                  <div className="flex items-center space-x-3">
                    <Folder
                      className={`w-5 h-5 ${
                        dir.status === 'ok'
                          ? 'text-emerald-500'
                          : dir.status === 'warning'
                          ? 'text-amber-500'
                          : 'text-gray-400'
                      }`}
                    />
                    <span className="text-sm font-medium text-gray-700">{dir.name}</span>
                  </div>
                  <div className="flex items-center space-x-2">
                    <span
                      className={`text-sm font-bold ${
                        dir.count === 0
                          ? 'text-gray-400'
                          : dir.count > 5
                          ? 'text-bronze-600'
                          : 'text-gray-600'
                      }`}
                    >
                      {dir.count}
                    </span>
                    {dir.status === 'ok' && <CheckCircle className="w-4 h-4 text-emerald-500" />}
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Recent Activity */}
          <div className="lg:col-span-2 bg-white rounded-2xl p-6 shadow-lg border border-gray-100">
            <div className="flex items-center space-x-3 mb-6">
              <Activity className="w-6 h-6 text-gold-600" />
              <h3 className="text-lg font-bold text-gray-900">Recent Activity</h3>
            </div>
            <div className="space-y-4">
              {data.recentActivity.map((activity, index) => (
                <div
                  key={index}
                  className="flex items-start space-x-4 p-4 bg-gradient-to-r from-gray-50 to-transparent rounded-xl hover:from-bronze-50 transition-all duration-300"
                >
                  <div
                    className={`w-10 h-10 rounded-full flex items-center justify-center flex-shrink-0 ${
                      activity.type === 'completion'
                        ? 'bg-emerald-100'
                        : activity.type === 'email'
                        ? 'bg-blue-100'
                        : activity.type === 'whatsapp'
                        ? 'bg-green-100'
                        : 'bg-blue-100'
                    }`}
                  >
                    {activity.type === 'completion' ? (
                      <CheckCircle className="w-5 h-5 text-emerald-600" />
                    ) : activity.type === 'email' ? (
                      <Mail className="w-5 h-5 text-blue-600" />
                    ) : activity.type === 'whatsapp' ? (
                      <MessageCircle className="w-5 h-5 text-green-600" />
                    ) : (
                      <Linkedin className="w-5 h-5 text-blue-600" />
                    )}
                  </div>
                  <div className="flex-1">
                    <p className="text-sm font-bold text-gray-900">{activity.action}</p>
                    <p className="text-sm text-gray-600 mt-1">{activity.description}</p>
                  </div>
                  <div className="text-right">
                    <p className="text-xs text-gray-500">{activity.timestamp.split(' ')[0]}</p>
                    <p className="text-xs text-gray-400">{activity.timestamp.split(' ')[1]}</p>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Plans Table */}
        {data.plans.length > 0 && (
          <div className="bg-white rounded-2xl p-6 shadow-lg border border-gray-100 mb-8">
            <div className="flex items-center space-x-3 mb-6">
              <Calendar className="w-6 h-6 text-bronze-600" />
              <h3 className="text-lg font-bold text-gray-900">Active Plans</h3>
            </div>
            <div className="overflow-x-auto">
              <table className="w-full">
                <thead>
                  <tr className="border-b border-gray-200">
                    <th className="text-left py-3 px-4 text-sm font-semibold text-gray-700">Plan Name</th>
                    <th className="text-left py-3 px-4 text-sm font-semibold text-gray-700">Priority</th>
                    <th className="text-left py-3 px-4 text-sm font-semibold text-gray-700">Tasks</th>
                    <th className="text-left py-3 px-4 text-sm font-semibold text-gray-700">Due Date</th>
                    <th className="text-left py-3 px-4 text-sm font-semibold text-gray-700">Status</th>
                  </tr>
                </thead>
                <tbody>
                  {data.plans.map((plan, index) => (
                    <tr
                      key={index}
                      className="border-b border-gray-100 hover:bg-gray-50 transition-colors"
                    >
                      <td className="py-3 px-4">
                        <span className={`text-sm font-medium ${plan.status === 'completed' ? 'line-through text-gray-400' : 'text-gray-900'}`}>
                          {plan.name}
                        </span>
                      </td>
                      <td className="py-3 px-4">
                        <span
                          className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${
                            plan.priority === 'P1'
                              ? 'bg-red-100 text-red-800'
                              : plan.priority === 'P2'
                              ? 'bg-amber-100 text-amber-800'
                              : 'bg-green-100 text-green-800'
                          }`}
                        >
                          {plan.priority}
                        </span>
                      </td>
                      <td className="py-3 px-4 text-sm text-gray-600">{plan.tasks}</td>
                      <td className="py-3 px-4">
                        <span className="text-sm text-gray-600">
                          {plan.due || 'No due date'}
                        </span>
                      </td>
                      <td className="py-3 px-4">
                        <span
                          className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${
                            plan.status === 'completed'
                              ? 'bg-emerald-100 text-emerald-800'
                              : plan.status === 'overdue'
                              ? 'bg-red-100 text-red-800'
                              : 'bg-blue-100 text-blue-800'
                          }`}
                        >
                          {plan.status === 'completed' && '✓ '}
                          {plan.status.charAt(0).toUpperCase() + plan.status.slice(1)}
                        </span>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        )}

        {/* Tags */}
        <div className="bg-white rounded-2xl p-6 shadow-lg border border-gray-100">
          <div className="flex items-center space-x-3 mb-4">
            <FileText className="w-6 h-6 text-gold-600" />
            <h3 className="text-lg font-bold text-gray-900">Metadata Tags</h3>
          </div>
          <div className="flex flex-wrap gap-2">
            {data.metadata.tags.map((tag, index) => (
              <span
                key={index}
                className="inline-flex items-center px-3 py-1.5 rounded-full text-sm font-medium bg-gradient-to-r from-bronze-100 to-gold-100 text-bronze-800 border border-bronze-200"
              >
                #{tag}
              </span>
            ))}
          </div>
          <div className="mt-4 pt-4 border-t border-gray-200">
            <div className="flex items-center justify-between">
              <p className="text-sm text-gray-600">
                Total Files Tracked: <span className="font-bold text-gray-900">{data.metadata.totalFilesTracked}</span>
              </p>
              <p className="text-xs text-gray-500">
                Dashboard fully operational
              </p>
            </div>
          </div>
        </div>
      </main>

      {/* Footer */}
      <footer className="bg-white/80 backdrop-blur-md border-t border-bronze-200 mt-12">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <div className="flex flex-col md:flex-row justify-between items-center">
            <p className="text-sm text-gray-600">
              © 2026 Bronze Tire Dashboard | AI Employee Operations
            </p>
            <div className="flex items-center space-x-4 mt-4 md:mt-0">
              <span className="text-xs text-gray-500">Powered by Next.js</span>
              <span className="text-gray-300">•</span>
              <span className="text-xs text-gray-500">Real-time Updates</span>
            </div>
          </div>
        </div>
      </footer>
    </div>
  );
}
