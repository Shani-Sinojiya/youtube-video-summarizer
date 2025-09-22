import Link from "next/link";
import Logo from "../logo";

export function Navigation() {
  return (
    <nav className="bg-white shadow-sm sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16">
          <div className="flex items-center">
            <Link href="/" className="flex-shrink-0 flex items-center">
              <div className="w-8 h-8 rounded-full bg-blue-900 flex items-center justify-center text-white font-bold text-sm mr-2">
                <Logo className="w-6 h-6" />
              </div>
              <span className="ml-3 text-xl font-semibold text-blue-900">
                Recapify
              </span>
            </Link>
          </div>
          <div className="hidden md:flex items-center space-x-8">
            <Link
              href="#features"
              className="text-gray-700 hover:text-orange-500 px-3 py-2 text-sm font-medium"
            >
              Features
            </Link>
            <Link
              href="#how-it-works"
              className="text-gray-700 hover:text-orange-500 px-3 py-2 text-sm font-medium"
            >
              How It Works
            </Link>
            <Link
              href="#testimonials"
              className="text-gray-700 hover:text-orange-500 px-3 py-2 text-sm font-medium"
            >
              Testimonials
            </Link>
            <Link
              href="#faq"
              className="text-gray-700 hover:text-orange-500 px-3 py-2 text-sm font-medium"
            >
              FAQ
            </Link>
          </div>
          <div className="flex items-center">
            <Link
              href="/login"
              className="bg-orange-500 hover:bg-orange-600 text-white px-4 py-2 rounded-full text-sm font-medium transition duration-300"
            >
              Get Started
            </Link>
          </div>
        </div>
      </div>
    </nav>
  );
}
