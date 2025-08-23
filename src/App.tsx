import React, { Suspense, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { useTranslation } from 'react-i18next';

// Layout Components
import Header from '@/components/layout/Header';
import Footer from '@/components/layout/Footer';
import LoadingSpinner from '@/components/common/LoadingSpinner';

// Pages - Lazy loaded for better performance
const HomePage = React.lazy(() => import('@/pages/HomePage'));
const AboutPage = React.lazy(() => import('@/pages/AboutPage'));
const BlogPage = React.lazy(() => import('@/pages/BlogPage'));
const BlogPostPage = React.lazy(() => import('@/pages/BlogPostPage'));
const LabPage = React.lazy(() => import('@/pages/LabPage'));
const ServicesPage = React.lazy(() => import('@/pages/ServicesPage'));
const ContactPage = React.lazy(() => import('@/pages/ContactPage'));
const NotFoundPage = React.lazy(() => import('@/pages/NotFoundPage'));

// Error Boundary Component
class ErrorBoundary extends React.Component<
  { children: React.ReactNode },
  { hasError: boolean; error?: Error }
> {
  constructor(props: { children: React.ReactNode }) {
    super(props);
    this.state = { hasError: false };
  }

  static getDerivedStateFromError(error: Error) {
    return { hasError: true, error };
  }

  componentDidCatch(error: Error, errorInfo: React.ErrorInfo) {
    console.error('Application error:', error, errorInfo);
  }

  render() {
    if (this.state.hasError) {
      return (
        <div className="min-h-screen flex items-center justify-center bg-gray-50">
          <div className="text-center">
            <h2 className="text-2xl font-bold text-gray-900 mb-4">Oops! Something went wrong</h2>
            <p className="text-gray-600 mb-6">We're sorry, but something unexpected happened.</p>
            <button
              className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
              onClick={() => window.location.reload()}
            >
              Reload Page
            </button>
          </div>
        </div>
      );
    }

    return this.props.children;
  }
}

const App: React.FC = () => {
  const { i18n } = useTranslation();

  // Update document language attribute
  useEffect(() => {
    document.documentElement.lang = i18n.language;
  }, [i18n.language]);

  // Update document title based on route
  useEffect(() => {
    const updateTitle = (title: string) => {
      document.title = `${title} | Wim Tilburgs - Smart Health AI Consultant`;
    };

    // Listen for route changes to update title
    const handleRouteChange = () => {
      const path = window.location.pathname;
      switch (path) {
        case '/':
          updateTitle('Home');
          break;
        case '/about':
          updateTitle('About');
          break;
        case '/blog':
          updateTitle('Blog');
          break;
        case '/lab':
          updateTitle('AI Lab');
          break;
        case '/services':
          updateTitle('Services');
          break;
        case '/contact':
          updateTitle('Contact');
          break;
        default:
          updateTitle('Smart Health AI');
      }
    };

    handleRouteChange();
    window.addEventListener('popstate', handleRouteChange);
    
    return () => {
      window.removeEventListener('popstate', handleRouteChange);
    };
  }, []);

  const PageLoadingFallback = () => (
    <div className="min-h-screen flex items-center justify-center">
      <LoadingSpinner />
    </div>
  );

  return (
    <ErrorBoundary>
      <Router>
        <div className="App min-h-screen bg-white">
          <Header />
          
          <main className="pt-16">
            <Suspense fallback={<PageLoadingFallback />}>
              <Routes>
                <Route path="/" element={<HomePage />} />
                <Route path="/about" element={<AboutPage />} />
                <Route path="/blog" element={<BlogPage />} />
                <Route path="/blog/:slug" element={<BlogPostPage />} />
                <Route path="/lab" element={<LabPage />} />
                <Route path="/lab/*" element={<LabPage />} />
                <Route path="/services" element={<ServicesPage />} />
                <Route path="/contact" element={<ContactPage />} />
                <Route path="*" element={<NotFoundPage />} />
              </Routes>
            </Suspense>
          </main>

          <Footer />
        </div>
      </Router>
    </ErrorBoundary>
  );
};

export default App;