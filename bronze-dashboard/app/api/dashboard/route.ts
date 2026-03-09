import { NextResponse } from 'next/server';
import { readFileSync } from 'fs';
import { join } from 'path';

export interface DashboardData {
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

export async function GET() {
  try {
    const bronzeVaultPath = join(process.cwd(), '..', 'Bronze Tire', 'AI_Employee_Vault');
    const dashboardPath = join(bronzeVaultPath, 'Dashboard.md');
    const donePath = join(bronzeVaultPath, 'Done');
    
    // Read dashboard markdown
    let dashboardContent = '';
    try {
      dashboardContent = readFileSync(dashboardPath, 'utf-8');
    } catch (error) {
      dashboardContent = '# No Dashboard Found';
    }

    // Parse dashboard content
    const lastUpdated = extractLastUpdated(dashboardContent);
    const quickStats = extractQuickStats(dashboardContent);
    const plans = extractPlans(dashboardContent);
    const completionReports = extractCompletionReports(dashboardContent);
    
    // Mock data for demonstration (in production, read from actual files)
    const directoryStatus = [
      { name: 'Inbox', count: 0, status: 'empty' as const },
      { name: 'Needs_Action', count: 0, status: 'empty' as const },
      { name: 'Plans', count: 10, status: 'ok' as const },
      { name: 'Done', count: 7, status: 'ok' as const },
      { name: 'Logs', count: 8, status: 'ok' as const },
    ];

    const recentActivity = [
      {
        action: 'Task Completion',
        description: 'Bronze Test Plan - 3 tasks completed',
        timestamp: '2026-03-06 12:00',
        type: 'completion' as const,
      },
      {
        action: 'Task Completion',
        description: 'Acme Corp Onboarding - 5 tasks completed',
        timestamp: '2026-03-06 12:00',
        type: 'completion' as const,
      },
      {
        action: 'Task Completion',
        description: 'Client Invoice Request - 3 tasks completed',
        timestamp: '2026-03-06 12:00',
        type: 'completion' as const,
      },
      {
        action: 'WhatsApp Sent',
        description: 'Message to +923322580130',
        timestamp: '2026-02-28 01:40',
        type: 'whatsapp' as const,
      },
      {
        action: 'Email Sent',
        description: 'Invoice to client@example.com',
        timestamp: '2026-02-24 21:45',
        type: 'email' as const,
      },
    ];

    const data: DashboardData = {
      lastUpdated,
      quickStats,
      directoryStatus,
      completionReports,
      recentActivity,
      plans,
      metadata: {
        totalFilesTracked: 5,
        tags: ['onboarding', 'enterprise', 'acme-corp', 'test', 'bronze-tier', 'invoice', 'completed'],
      },
    };

    return NextResponse.json(data);
  } catch (error) {
    console.error('Error fetching dashboard data:', error);
    return NextResponse.json({ error: 'Failed to fetch dashboard data' }, { status: 500 });
  }
}

function extractLastUpdated(content: string): string {
  const match = content.match(/\*\*Last Updated:\*\*\s*(.+)/);
  return match ? match[1].trim() : new Date().toISOString().split('T')[0];
}

function extractQuickStats(content: string) {
  const pendingMatch = content.match(/Pending Tasks:\s*(\d+)/);
  const activePlansMatch = content.match(/Active Plans:\s*(\d+)/);
  const completedPlansMatch = content.match(/Completed Plans:\s*(\d+)/);
  
  return {
    pendingTasks: parseInt(pendingMatch?.[1] || '0'),
    completedTasks: 11,
    activePlans: parseInt(activePlansMatch?.[1] || '0'),
    completedPlans: parseInt(completedPlansMatch?.[1] || '3'),
  };
}

function extractPlans(content: string) {
  const plans = [];
  const planMatches = content.matchAll(/\|\s*~~?([^|]+)~~?\s*\|\s*([Pp]\d+)\s*\|\s*~~?(\d+)~~?\s*\|\s*~~?([^|]+)~~?\s*\|\s*(?:✅\s*)?([A-Z]+)/g);
  
  for (const match of planMatches) {
    plans.push({
      name: match[1].trim(),
      priority: match[2].toUpperCase() as 'P1' | 'P2' | 'P3',
      tasks: parseInt(match[3]),
      due: match[4].trim() !== '-' ? match[4].trim() : null,
      status: match[5].includes('COMPLETED') ? 'completed' as const : 'active' as const,
    });
  }
  
  return plans;
}

function extractCompletionReports(content: string) {
  const reports = [];
  const reportMatches = content.matchAll(/\|\s*(COMPLETION_[^|]+)\s*\|\s*([^|]+)\s*\|\s*(\d+)\s*✅/g);
  
  for (const match of reportMatches) {
    reports.push({
      title: match[1].trim().replace('.md', ''),
      date: match[2].trim(),
      tasksCompleted: parseInt(match[3]),
    });
  }
  
  return reports;
}
