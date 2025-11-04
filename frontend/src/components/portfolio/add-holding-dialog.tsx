'use client';

import { useState } from 'react';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from '@/components/ui/dialog';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select';
import type { AddHoldingRequest } from '@/types/portfolio';

const holdingSchema = z.object({
  asset_type: z.enum(['equity', 'debt', 'gold', 'international']),
  asset_name: z.string().min(1, 'Asset name is required'),
  quantity: z.number().positive('Quantity must be positive'),
  current_price: z.number().positive('Current price must be positive'),
  purchase_price: z.number().positive('Purchase price must be positive'),
  allocation: z.number().min(0).max(100, 'Allocation must be between 0 and 100'),
});

interface AddHoldingDialogProps {
  portfolioId: number;
  onSubmit: (data: AddHoldingRequest) => Promise<void>;
  trigger?: React.ReactNode;
}

export function AddHoldingDialog({ portfolioId, onSubmit, trigger }: AddHoldingDialogProps) {
  const [open, setOpen] = useState(false);
  const [isLoading, setIsLoading] = useState(false);

  const form = useForm<z.infer<typeof holdingSchema>>({
    resolver: zodResolver(holdingSchema),
    defaultValues: {
      asset_type: 'equity',
      asset_name: '',
      quantity: 0,
      current_price: 0,
      purchase_price: 0,
      allocation: 0,
    },
  });

  const handleSubmit = async (data: z.infer<typeof holdingSchema>) => {
    setIsLoading(true);
    try {
      await onSubmit({
        portfolio_id: portfolioId,
        ...data,
      });
      setOpen(false);
      form.reset();
    } catch (error) {
      console.error('Failed to add holding:', error);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <Dialog open={open} onOpenChange={setOpen}>
      <DialogTrigger asChild>
        {trigger || <Button>Add Holding</Button>}
      </DialogTrigger>
      <DialogContent>
        <DialogHeader>
          <DialogTitle>Add Holding</DialogTitle>
          <DialogDescription>Add a new asset to your portfolio</DialogDescription>
        </DialogHeader>
        <form onSubmit={form.handleSubmit(handleSubmit)} className="space-y-4">
          <div className="space-y-2">
            <Label htmlFor="asset_type">Asset Type</Label>
            <Select
              value={form.watch('asset_type')}
              onValueChange={(value) => form.setValue('asset_type', value as any)}
            >
              <SelectTrigger>
                <SelectValue />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="equity">Equity</SelectItem>
                <SelectItem value="debt">Debt</SelectItem>
                <SelectItem value="gold">Gold</SelectItem>
                <SelectItem value="international">International</SelectItem>
              </SelectContent>
            </Select>
          </div>

          <div className="space-y-2">
            <Label htmlFor="asset_name">Asset Name</Label>
            <Input id="asset_name" {...form.register('asset_name')} />
            {form.formState.errors.asset_name && (
              <p className="text-sm text-destructive">{form.formState.errors.asset_name.message}</p>
            )}
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div className="space-y-2">
              <Label htmlFor="quantity">Quantity</Label>
              <Input
                id="quantity"
                type="number"
                step="0.01"
                {...form.register('quantity', { valueAsNumber: true })}
              />
            </div>
            <div className="space-y-2">
              <Label htmlFor="allocation">Allocation (%)</Label>
              <Input
                id="allocation"
                type="number"
                step="0.01"
                {...form.register('allocation', { valueAsNumber: true })}
              />
            </div>
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div className="space-y-2">
              <Label htmlFor="current_price">Current Price (₹)</Label>
              <Input
                id="current_price"
                type="number"
                step="0.01"
                {...form.register('current_price', { valueAsNumber: true })}
              />
            </div>
            <div className="space-y-2">
              <Label htmlFor="purchase_price">Purchase Price (₹)</Label>
              <Input
                id="purchase_price"
                type="number"
                step="0.01"
                {...form.register('purchase_price', { valueAsNumber: true })}
              />
            </div>
          </div>

          <div className="flex justify-end gap-2">
            <Button type="button" variant="outline" onClick={() => setOpen(false)}>
              Cancel
            </Button>
            <Button type="submit" disabled={isLoading}>
              {isLoading ? 'Adding...' : 'Add Holding'}
            </Button>
          </div>
        </form>
      </DialogContent>
    </Dialog>
  );
}

