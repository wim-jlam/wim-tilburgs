// Common types
export type Language = 'nl' | 'en';

export interface LocalizedString {
  nl: string;
  en: string;
}

// API Response types
export interface ApiResponse<T> {
  success: boolean;
  data: T;
  message?: string;
  error?: string;
}

export interface PaginatedResponse<T> {
  items: T[];
  total: number;
  page: number;
  per_page: number;
  total_pages: number;
}

// Blog types
export interface BlogPost {
  id: string;
  slug: string;
  title: LocalizedString;
  content: LocalizedString;
  excerpt: LocalizedString;
  author: {
    id: string;
    name: string;
    avatar_url?: string;
  };
  featured_image?: string;
  tags: string[];
  categories: string[];
  seo: {
    description: LocalizedString;
    keywords: string[];
  };
  published: boolean;
  auto_translated: boolean;
  created_at: string;
  updated_at: string;
  published_at?: string;
  read_time: number; // estimated minutes
}

export interface BlogCategory {
  id: string;
  name: LocalizedString;
  slug: string;
  description: LocalizedString;
  post_count: number;
  color?: string;
}

export interface BlogTag {
  id: string;
  name: string;
  slug: string;
  post_count: number;
}

// Menu/Navigation types
export interface MenuItem {
  id: string;
  label: LocalizedString;
  path: string;
  icon?: string;
  children?: MenuItem[];
  external?: boolean;
  order: number;
  visible: boolean;
}

// Page content types
export interface Page {
  id: string;
  slug: string;
  title: LocalizedString;
  content: LocalizedString;
  meta_description: LocalizedString;
  published: boolean;
  updated_at: string;
}

// User types
export interface User {
  id: string;
  email: string;
  name: string;
  role: 'admin' | 'author' | 'user';
  avatar_url?: string;
  bio?: LocalizedString;
  created_at: string;
}

// Component props
export interface BaseComponentProps {
  className?: string;
  children?: React.ReactNode;
}

export interface LanguageSwitcherProps {
  currentLanguage: Language;
  onLanguageChange: (language: Language) => void;
}

// Form types
export interface ContactForm {
  name: string;
  email: string;
  company?: string;
  message: string;
  subject: string;
}

// Search/Filter types
export interface BlogFilters {
  search?: string;
  category?: string;
  tag?: string;
  author?: string;
  published_after?: string;
  published_before?: string;
}

export interface BlogSearchParams {
  page: number;
  per_page: number;
  language: Language;
  filters: BlogFilters;
}