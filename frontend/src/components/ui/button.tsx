import type { ButtonHTMLAttributes } from 'react'
import { cn } from '@/lib/utils'

export const buttonClass =
  'inline-flex min-h-9 cursor-pointer items-center justify-center gap-2 border border-primary bg-primary px-4 py-1.5 font-semibold tracking-wide text-primary-foreground no-underline transition-colors hover:bg-primary/85 active:translate-y-px disabled:cursor-not-allowed disabled:opacity-60'

export function Button({
  className,
  type = 'button',
  ...props
}: ButtonHTMLAttributes<HTMLButtonElement>) {
  return <button type={type} className={cn(buttonClass, className)} {...props} />
}
