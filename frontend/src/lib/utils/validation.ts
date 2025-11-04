import { z } from 'zod';

/**
 * Email validation schema
 */
export const emailSchema = z.string().email('Invalid email address');

/**
 * Phone number validation (Indian format)
 */
export const phoneSchema = z.string().regex(/^[6-9]\d{9}$/, 'Invalid phone number');

/**
 * Password validation
 */
export const passwordSchema = z.string().min(8, 'Password must be at least 8 characters');

/**
 * Positive number validation
 */
export const positiveNumberSchema = z.number().positive('Must be a positive number');

/**
 * Percentage validation (0-100)
 */
export const percentageSchema = z.number().min(0).max(100, 'Percentage must be between 0 and 100');

