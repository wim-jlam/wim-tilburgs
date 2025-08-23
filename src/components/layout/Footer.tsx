import React from 'react';
import { Link } from 'react-router-dom';
import { useTranslation } from 'react-i18next';

const Footer: React.FC = () => {
  const { t } = useTranslation();
  const currentYear = new Date().getFullYear();

  const navigation = {
    main: [
      { name: t('nav.home'), href: '/' },
      { name: t('nav.about'), href: '/about' },
      { name: t('nav.blog'), href: '/blog' },
      { name: t('nav.lab'), href: '/lab' },
      { name: t('nav.services'), href: '/services' },
      { name: t('nav.contact'), href: '/contact' },
    ],
    social: [
      {
        name: 'LinkedIn',
        href: 'https://linkedin.com/in/wimtilburgs',
        icon: (
          <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 20 20" aria-hidden="true">
            <path d="M16.338 16.338H13.67V12.16c0-.995-.017-2.277-1.387-2.277-1.39 0-1.601 1.086-1.601 2.207v4.248H8.014v-8.59h2.559v1.174h.037c.356-.675 1.227-1.387 2.526-1.387 2.703 0 3.203 1.778 3.203 4.092v4.711zM5.005 6.575a1.548 1.548 0 11-.003-3.096 1.548 1.548 0 01.003 3.096zm-1.337 9.763H6.34v-8.59H3.667v8.59zM17.668 1H2.328C1.595 1 1 1.581 1 2.298v15.403C1 18.418 1.595 19 2.328 19h15.34c.734 0 1.332-.582 1.332-1.299V2.298C19 1.581 18.402 1 17.668 1z" />
          </svg>
        ),
      },
      {
        name: 'Twitter/X',
        href: 'https://twitter.com/wimtilburgs',
        icon: (
          <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 20 20" aria-hidden="true">
            <path d="M15.751 2.75h2.854l-6.232 7.124 7.327 9.676h-5.742l-4.493-5.876-5.14 5.876H1.471l6.667-7.619L1.216 2.75h5.89l4.063 5.373L15.75 2.75zm-1.002 14.397h1.581L6.084 4.356H4.395l10.354 12.791z" />
          </svg>
        ),
      },
      {
        name: 'GitHub',
        href: 'https://github.com/wimtilburgs',
        icon: (
          <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 20 20" aria-hidden="true">
            <path
              fillRule="evenodd"
              d="M10 0C4.477 0 0 4.484 0 10.017c0 4.425 2.865 8.18 6.839 9.504.5.092.682-.217.682-.483 0-.237-.008-.868-.013-1.703-2.782.605-3.369-1.343-3.369-1.343-.454-1.158-1.11-1.466-1.11-1.466-.908-.62.069-.608.069-.608 1.003.07 1.531 1.032 1.531 1.032.892 1.53 2.341 1.088 2.91.832.092-.647.35-1.088.636-1.338-2.22-.253-4.555-1.113-4.555-4.951 0-1.093.39-1.988 1.029-2.688-.103-.253-.446-1.272.098-2.65 0 0 .84-.27 2.75 1.026A9.564 9.564 0 0110 4.844c.85.004 1.705.115 2.504.337 1.909-1.296 2.747-1.027 2.747-1.027.546 1.379.203 2.398.1 2.651.64.7 1.028 1.595 1.028 2.688 0 3.848-2.339 4.695-4.566 4.942.359.31.678.921.678 1.856 0 1.338-.012 2.419-.012 2.747 0 .268.18.58.688.482A10.019 10.019 0 0020 10.017C20 4.484 15.522 0 10 0z"
              clipRule="evenodd"
            />
          </svg>
        ),
      },
      {
        name: 'YouTube',
        href: 'https://youtube.com/@jlamcommunity',
        icon: (
          <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 20 20" aria-hidden="true">
            <path d="M2.838 5.715c-.893.22-1.592.871-1.823 1.699C.687 8.708.687 12 .687 12s0 3.293.328 4.586c.23.828.93 1.48 1.823 1.699C4.287 18.629 10 18.629 10 18.629s5.713 0 7.162-.344c.893-.22 1.593-.871 1.823-1.699.328-1.293.328-4.586.328-4.586s0-3.292-.328-4.585c-.23-.828-.93-1.48-1.823-1.699C15.713 5.371 10 5.371 10 5.371s-5.713 0-7.162.344zM8.109 9.626V14.374L13.281 12l-5.172-2.374z" />
          </svg>
        ),
      },
    ],
  };

  return (
    <footer className="bg-gray-50 border-t border-gray-200">
      <div className="container mx-auto px-4 py-12 sm:px-6 lg:px-8">
        <div className="xl:grid xl:grid-cols-3 xl:gap-8">
          {/* Logo & Tagline */}
          <div className="xl:col-span-1">
            <Link to="/" className="flex items-center space-x-2 mb-4">
              <div className="w-10 h-10 bg-gradient-to-br from-blue-600 to-purple-600 rounded-lg flex items-center justify-center">
                <span className="text-white font-bold text-lg">WT</span>
              </div>
              <div>
                <span className="text-xl font-bold text-gray-900">Wim Tilburgs</span>
                <div className="text-sm text-gray-600">Smart Health AI</div>
              </div>
            </Link>
            <p className="text-gray-600 mb-6 max-w-md">
              {t('footer.tagline')} - Van 125kg diabeet naar AI health pioneer.
            </p>
            <div className="flex space-x-6">
              {navigation.social.map((item) => (
                <a
                  key={item.name}
                  href={item.href}
                  className="text-gray-400 hover:text-gray-600 transition-colors duration-200"
                  target="_blank"
                  rel="noopener noreferrer"
                  aria-label={`Follow on ${item.name}`}
                >
                  {item.icon}
                </a>
              ))}
            </div>
          </div>

          {/* Navigation Links */}
          <div className="mt-12 xl:mt-0 xl:col-span-2">
            <div className="grid grid-cols-2 gap-8 md:grid-cols-3">
              <div>
                <h3 className="text-sm font-semibold text-gray-900 tracking-wider uppercase mb-4">
                  Navigation
                </h3>
                <ul className="space-y-3">
                  {navigation.main.map((item) => (
                    <li key={item.name}>
                      <Link
                        to={item.href}
                        className="text-gray-600 hover:text-gray-900 transition-colors duration-200"
                      >
                        {item.name}
                      </Link>
                    </li>
                  ))}
                </ul>
              </div>

              <div>
                <h3 className="text-sm font-semibold text-gray-900 tracking-wider uppercase mb-4">
                  AI Research
                </h3>
                <ul className="space-y-3">
                  <li>
                    <Link
                      to="/lab/gpt5"
                      className="text-gray-600 hover:text-gray-900 transition-colors duration-200"
                    >
                      GPT-5 Health Research
                    </Link>
                  </li>
                  <li>
                    <Link
                      to="/lab/tools"
                      className="text-gray-600 hover:text-gray-900 transition-colors duration-200"
                    >
                      AI Health Tools
                    </Link>
                  </li>
                  <li>
                    <Link
                      to="/lab/community"
                      className="text-gray-600 hover:text-gray-900 transition-colors duration-200"
                    >
                      Developer Community
                    </Link>
                  </li>
                  <li>
                    <a
                      href="https://jlam.nl"
                      className="text-gray-600 hover:text-gray-900 transition-colors duration-200"
                      target="_blank"
                      rel="noopener noreferrer"
                    >
                      JLAM Platform
                    </a>
                  </li>
                </ul>
              </div>

              <div>
                <h3 className="text-sm font-semibold text-gray-900 tracking-wider uppercase mb-4">
                  Legal
                </h3>
                <ul className="space-y-3">
                  <li>
                    <Link
                      to="/privacy"
                      className="text-gray-600 hover:text-gray-900 transition-colors duration-200"
                    >
                      {t('footer.privacy')}
                    </Link>
                  </li>
                  <li>
                    <Link
                      to="/terms"
                      className="text-gray-600 hover:text-gray-900 transition-colors duration-200"
                    >
                      {t('footer.terms')}
                    </Link>
                  </li>
                  <li>
                    <Link
                      to="/cookies"
                      className="text-gray-600 hover:text-gray-900 transition-colors duration-200"
                    >
                      Cookie Policy
                    </Link>
                  </li>
                </ul>
              </div>
            </div>
          </div>
        </div>

        {/* Bottom Border */}
        <div className="mt-12 pt-8 border-t border-gray-200">
          <div className="flex flex-col md:flex-row md:items-center md:justify-between">
            <p className="text-gray-500 text-sm">
              © {currentYear} Wim Tilburgs. All rights reserved.
            </p>
            <p className="text-gray-500 text-sm mt-2 md:mt-0">
              Built with React, TypeScript & AI ❤️
            </p>
          </div>
        </div>
      </div>
    </footer>
  );
};

export default Footer;