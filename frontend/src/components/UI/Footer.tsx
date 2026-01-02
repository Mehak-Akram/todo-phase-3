import Link from 'next/link';

const Footer = () => {
  return (
    <footer className="bg-gradient-to-t from-blue-500/20 to-blue-600/20 backdrop-blur-lg border-t border-white/20 py-8">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex flex-col md:flex-row justify-between items-center">
          <div className="mb-4 md:mb-0">
            <h3 className="text-lg font-semibold text-purple-500">Todo App</h3>
            <p className="text-black-900 mt-1">Stay organized, stay productive</p>
          </div>

          <div className="flex flex-wrap justify-center gap-6">
            <div>
              <h4 className="text-sm font-semibold text-black-900 uppercase tracking-wider">Product</h4>
              <ul className="mt-2 space-y-2">
                <li>
                  <Link href="/" className="text-black-900 hover:text-purple-500">
                    Features
                  </Link>
                </li>
                <li>
                  <Link href="/" className="text-black-900 hover:text-purple-500">
                    Pricing
                  </Link>
                </li>
                <li>
                  <Link href="/" className="text-black-900 hover:text-purple-500">
                    Documentation
                  </Link>
                </li>
              </ul>
            </div>

            <div>
              <h4 className="text-sm font-semibold text-black-900 uppercase tracking-wider">Company</h4>
              <ul className="mt-2 space-y-2">
                <li>
                  <Link href="/" className="text-black-900 hover:text-purple-500">
                    About
                  </Link>
                </li>
                <li>
                  <Link href="/" className="text-black-900 hover:text-purple-500">
                    Contact
                  </Link>
                </li>
                <li>
                  <Link href="/" className="text-black-900 hover:text-purple-500">
                    Careers
                  </Link>
                </li>
              </ul>
            </div>

            <div>
              <h4 className="text-sm font-semibold text-black-900 uppercase tracking-wider">Legal</h4>
              <ul className="mt-2 space-y-2">
                <li>
                  <Link href="/" className="text-black-900 hover:text-purple-500">
                    Privacy
                  </Link>
                </li>
                <li>
                  <Link href="/" className="text-black-900 hover:text-purple-500">
                    Terms
                  </Link>
                </li>
                <li>
                  <Link href="/" className="text-black-900 hover:text-purple-500">
                    Cookies
                  </Link>
                </li>
              </ul>
            </div>
          </div>
        </div>

        <div className="mt-8 pt-8 border-t border-white/20 flex flex-col md:flex-row justify-between items-center">
          <p className="text-black-900 text-sm">
            &copy; {new Date().getFullYear()} Todo App. All rights reserved.
          </p>
          <div className="mt-4 md:mt-0 flex space-x-6">
            <a href="#" className="text-black-900 hover:text-purple-500">
              <span className="sr-only">Twitter</span>
              <svg className="h-6 w-6" fill="currentColor" viewBox="0 0 24 24">
                <path d="M8.29 20.251c7.547 0 11.675-6.253 11.675-11.675 0-.178 0-.355-.012-.53A8.348 8.348 0 0022 5.92a8.19 8.19 0 01-2.357.646 4.118 4.118 0 001.804-2.27 8.224 8.224 0 01-2.605.996 4.107 4.107 0 00-6.993 3.743 11.65 11.65 0 01-8.457-4.287 4.106 4.106 0 001.27 5.477A4.072 4.072 0 012.8 9.713v.052a4.105 4.105 0 003.292 4.022 4.095 4.095 0 01-1.853.07 4.108 4.108 0 003.834 2.85A8.233 8.233 0 012 18.407a11.616 11.616 0 006.29 1.84" />
              </svg>
            </a>
            <a href="#" className="text-black-900 hover:text-purple-500">
              <span className="sr-only">GitHub</span>
              <svg className="h-6 w-6" fill="currentColor" viewBox="0 0 24 24">
                <path fillRule="evenodd" d="M12 2C6.477 2 2 6.484 2 12.017c0 4.425 2.865 8.18 6.839 9.504.5.092.682-.217.682-.483 0-.237-.008-.868-.013-1.703-2.782.605-3.369-1.343-3.369-1.343-.454-1.158-1.11-1.466-1.11-1.466-.908-.62.069-.608.069-.608 1.003.07 1.531 1.032 1.531 1.032.892 1.53 2.341 1.088 2.91.832.092-.647.35-1.088.636-1.338-2.22-.253-4.555-1.113-4.555-4.951 0-1.093.39-1.988 1.029-2.688-.103-.253-.446-1.272.098-2.65 0 0 .84-.27 2.75 1.026A9.564 9.564 0 0112 6.844c.85.004 1.705.115 2.504.337 1.909-1.296 2.747-1.027 2.747-1.027.546 1.379.202 2.398.1 2.651.64.7 1.028 1.595 1.028 2.688 0 3.848-2.339 4.695-4.566 4.943.359.309.678.92.678 1.855 0 1.338-.012 2.419-.012 2.747 0 .268.18.58.688.482A10.019 10.019 0 0022 12.017C22 6.484 17.522 2 12 2z" clipRule="evenodd" />
              </svg>
            </a>
          </div>
        </div>
      </div>
    </footer>
  );
};

export default Footer;