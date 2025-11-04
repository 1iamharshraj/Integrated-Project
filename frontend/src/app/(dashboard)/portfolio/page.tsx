'use client';

import { useEffect, useState } from 'react';
import { useAuthStore } from '@/store/auth-store';
import { usePortfolioStore } from '@/store/portfolio-store';
import { PortfolioSummary } from '@/components/portfolio/portfolio-summary';
import { HoldingsTable } from '@/components/portfolio/holdings-table';
import { AssetAllocationChart } from '@/components/portfolio/asset-allocation-chart';
import { AddHoldingDialog } from '@/components/portfolio/add-holding-dialog';
import { Button } from '@/components/ui/button';
import { portfolioApi } from '@/lib/api/portfolio';
import { Plus } from 'lucide-react';

export default function PortfolioPage() {
  const { user } = useAuthStore();
  const { portfolio, holdings, performance, fetchPortfolio } = usePortfolioStore();
  const [isAdding, setIsAdding] = useState(false);

  useEffect(() => {
    if (user?.id) {
      fetchPortfolio(user.id);
    }
  }, [user, fetchPortfolio]);

  const handleAddHolding = async (data: any) => {
    if (portfolio) {
      await portfolioApi.addHolding(data);
      await fetchPortfolio(user!.id);
    }
  };

  const handleDeleteHolding = async (holdingId: number) => {
    await portfolioApi.deleteHolding(holdingId);
    await fetchPortfolio(user!.id);
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold">Portfolio</h1>
          <p className="text-muted-foreground">Manage your investment portfolio</p>
        </div>
        {portfolio && (
          <AddHoldingDialog
            portfolioId={portfolio.id}
            onSubmit={handleAddHolding}
            trigger={
              <Button>
                <Plus className="mr-2 h-4 w-4" /> Add Holding
              </Button>
            }
          />
        )}
      </div>

      <PortfolioSummary portfolio={portfolio} performance={performance} />

      <div className="grid gap-6 md:grid-cols-2">
        <AssetAllocationChart performance={performance} />
        <div className="space-y-6">
          {/* Performance chart can be added here */}
        </div>
      </div>

      <HoldingsTable
        holdings={holdings}
        onDelete={handleDeleteHolding}
      />
    </div>
  );
}
