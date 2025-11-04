import Link from 'next/link';

export function Footer() {
  return (
    <footer className="border-t bg-background">
      <div className="container px-4 py-12">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
          <div>
            <div className="flex items-center space-x-2 mb-4">
              <div className="fintech-gradient h-8 w-8 rounded-lg flex items-center justify-center">
                <span className="text-white font-bold text-lg">Z</span>
              </div>
              <span className="font-bold text-xl">ZeTheta FinArcade</span>
            </div>
            <p className="text-sm text-muted-foreground">
              India's first fully autonomous AI-driven investment advisory platform.
            </p>
          </div>

          <div>
            <h3 className="font-semibold mb-4">Platform</h3>
            <ul className="space-y-2 text-sm">
              <li>
                <Link href="/dashboard" className="text-muted-foreground hover:text-foreground">
                  Dashboard
                </Link>
              </li>
              <li>
                <Link href="/portfolio" className="text-muted-foreground hover:text-foreground">
                  Portfolio
                </Link>
              </li>
              <li>
                <Link href="/risk-profiling" className="text-muted-foreground hover:text-foreground">
                  Risk Profiling
                </Link>
              </li>
              <li>
                <Link href="/goals" className="text-muted-foreground hover:text-foreground">
                  Goals
                </Link>
              </li>
            </ul>
          </div>

          <div>
            <h3 className="font-semibold mb-4">Resources</h3>
            <ul className="space-y-2 text-sm">
              <li>
                <Link href="/education" className="text-muted-foreground hover:text-foreground">
                  Education
                </Link>
              </li>
              <li>
                <Link href="/market" className="text-muted-foreground hover:text-foreground">
                  Market Data
                </Link>
              </li>
              <li>
                <Link href="/ai-insights" className="text-muted-foreground hover:text-foreground">
                  AI Insights
                </Link>
              </li>
            </ul>
          </div>

          <div>
            <h3 className="font-semibold mb-4">Company</h3>
            <ul className="space-y-2 text-sm">
              <li>
                <Link href="/pricing" className="text-muted-foreground hover:text-foreground">
                  Pricing
                </Link>
              </li>
              <li>
                <Link href="/about" className="text-muted-foreground hover:text-foreground">
                  About
                </Link>
              </li>
              <li>
                <Link href="/contact" className="text-muted-foreground hover:text-foreground">
                  Contact
                </Link>
              </li>
            </ul>
          </div>
        </div>

        <div className="mt-8 pt-8 border-t text-center text-sm text-muted-foreground">
          <p>&copy; {new Date().getFullYear()} ZeTheta FinArcade. All rights reserved.</p>
        </div>
      </div>
    </footer>
  );
}

