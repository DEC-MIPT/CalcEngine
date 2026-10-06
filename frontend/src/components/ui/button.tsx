import type { ButtonHTMLAttributes } from 'react'
import { cn } from '@/lib/utils'

export function Button({
  className,
  type = 'button',
  ...props
}: ButtonHTMLAttributes<HTMLButtonElement>) {
  return (
    <button
      type={type}
      className={cn(
        'inline-flex min-h-9 cursor-pointer items-center justify-center gap-2 border border-primary bg-primary px-4 py-1.5 font-medium text-primary-foreground transition-colors hover:bg-primary/90',
        className,
      )}
      {...props}
    />
  )
}
