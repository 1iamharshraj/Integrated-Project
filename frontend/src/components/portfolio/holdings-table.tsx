'use client';

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { formatCurrency, formatPercentage } from '@/lib/utils/format';
import type { Holding } from '@/types/portfolio';
import { Edit, Trash2 } from 'lucide-react';

interface HoldingsTableProps {
  holdings: Holding[];
  onEdit?: (holding: Holding) => void;
  onDelete?: (holdingId: number) => void;
}

export function HoldingsTable({ holdings, onEdit, onDelete }: HoldingsTableProps) {
  if (holdings.length === 0) {
    return (
      <Card>
        <CardHeader>
          <CardTitle>Holdings</CardTitle>
          <CardDescription>Your portfolio holdings</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="text-center py-8 text-muted-foreground">
            No holdings yet. Add your first holding to get started.
          </div>
        </CardContent>
      </Card>
    );
  }

  return (
    <Card>
      <CardHeader>
        <CardTitle>Holdings</CardTitle>
        <CardDescription>Your portfolio holdings</CardDescription>
      </CardHeader>
      <CardContent>
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead>
              <tr className="border-b">
                <th className="text-left p-4">Asset</th>
                <th className="text-left p-4">Type</th>
                <th className="text-right p-4">Quantity</th>
                <th className="text-right p-4">Current Price</th>
                <th className="text-right p-4">Value</th>
                <th className="text-right p-4">Gain/Loss</th>
                <th className="text-right p-4">Allocation</th>
                <th className="text-center p-4">Actions</th>
              </tr>
            </thead>
            <tbody>
              {holdings.map((holding) => {
                const gainLoss = (holding.current_price - holding.purchase_price) * holding.quantity;
                const gainLossPercent = ((holding.current_price - holding.purchase_price) / holding.purchase_price) * 100;
                const currentValue = holding.current_price * holding.quantity;

                return (
                  <tr key={holding.id} className="border-b hover:bg-muted/50">
                    <td className="p-4 font-medium">{holding.asset_name}</td>
                    <td className="p-4">
                      <Badge variant="outline">{holding.asset_type}</Badge>
                    </td>
                    <td className="p-4 text-right">{holding.quantity}</td>
                    <td className="p-4 text-right">{formatCurrency(holding.current_price)}</td>
                    <td className="p-4 text-right font-medium">{formatCurrency(currentValue)}</td>
                    <td className={`p-4 text-right ${gainLoss >= 0 ? 'text-success' : 'text-destructive'}`}>
                      {formatPercentage(gainLossPercent)}
                    </td>
                    <td className="p-4 text-right">{holding.allocation.toFixed(2)}%</td>
                    <td className="p-4">
                      <div className="flex justify-center gap-2">
                        {onEdit && (
                          <Button variant="ghost" size="icon" onClick={() => onEdit(holding)}>
                            <Edit className="h-4 w-4" />
                          </Button>
                        )}
                        {onDelete && (
                          <Button variant="ghost" size="icon" onClick={() => onDelete(holding.id)}>
                            <Trash2 className="h-4 w-4 text-destructive" />
                          </Button>
                        )}
                      </div>
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      </CardContent>
    </Card>
  );
}

