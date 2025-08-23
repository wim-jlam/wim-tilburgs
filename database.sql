-- PostgreSQL Schema for wimtilburgs.nl
-- Tweetalig blog platform met menu ondersteuning
-- Created: August 23, 2025

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Users table
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    email VARCHAR(255) UNIQUE NOT NULL,
    name VARCHAR(255) NOT NULL,
    role VARCHAR(50) DEFAULT 'author' CHECK (role IN ('admin', 'author', 'editor', 'user')),
    avatar_url VARCHAR(500),
    bio JSONB, -- {"nl": "Bio NL", "en": "Bio EN"}
    
    -- Authentication
    password_hash VARCHAR(255),
    email_verified BOOLEAN DEFAULT false,
    email_verified_at TIMESTAMP WITH TIME ZONE,
    
    -- Settings
    preferred_language VARCHAR(2) DEFAULT 'nl' CHECK (preferred_language IN ('nl', 'en')),
    timezone VARCHAR(100) DEFAULT 'Europe/Amsterdam',
    
    -- Metadata
    last_login_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Categories table for blog organization
CREATE TABLE blog_categories (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    slug VARCHAR(255) UNIQUE NOT NULL,
    name JSONB NOT NULL, -- {"nl": "Categorie NL", "en": "Category EN"}
    description JSONB, -- {"nl": "Beschrijving NL", "en": "Description EN"}
    color VARCHAR(7), -- Hex color code #000000
    
    -- SEO
    meta_description JSONB,
    
    -- Hierarchy support
    parent_id UUID REFERENCES blog_categories(id) ON DELETE SET NULL,
    sort_order INTEGER DEFAULT 0,
    
    -- Status
    published BOOLEAN DEFAULT true,
    
    -- Metadata
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Blog posts table - core content
CREATE TABLE blog_posts (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    slug VARCHAR(255) UNIQUE NOT NULL,
    
    -- Multilingual content
    title JSONB NOT NULL, -- {"nl": "Titel", "en": "Title"}
    content JSONB NOT NULL, -- {"nl": "Content NL", "en": "Content EN"}
    excerpt JSONB NOT NULL, -- {"nl": "Samenvatting", "en": "Summary"}
    
    -- SEO
    meta_title JSONB,
    meta_description JSONB NOT NULL,
    meta_keywords TEXT[], -- Array of keywords
    canonical_url VARCHAR(500),
    
    -- Media
    featured_image VARCHAR(500),
    featured_image_alt JSONB, -- {"nl": "Alt NL", "en": "Alt EN"}
    
    -- Organization
    author_id UUID NOT NULL REFERENCES users(id) ON DELETE RESTRICT,
    category_id UUID REFERENCES blog_categories(id) ON DELETE SET NULL,
    
    -- Content metadata
    reading_time_minutes INTEGER,
    word_count INTEGER,
    
    -- Status & Publishing
    status VARCHAR(20) DEFAULT 'draft' CHECK (status IN ('draft', 'published', 'archived')),
    published_at TIMESTAMP WITH TIME ZONE,
    
    -- AI & Translation
    auto_translated BOOLEAN DEFAULT false,
    original_language VARCHAR(2) DEFAULT 'nl' CHECK (original_language IN ('nl', 'en')),
    translation_quality_score DECIMAL(3,2), -- 0.00 to 1.00
    
    -- Engagement
    view_count INTEGER DEFAULT 0,
    like_count INTEGER DEFAULT 0,
    
    -- Timestamps
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Tags table
CREATE TABLE blog_tags (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(100) UNIQUE NOT NULL,
    slug VARCHAR(100) UNIQUE NOT NULL,
    color VARCHAR(7), -- Hex color
    description TEXT,
    
    -- Usage stats
    post_count INTEGER DEFAULT 0,
    
    -- Metadata
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Many-to-many relationship: posts <-> tags
CREATE TABLE blog_post_tags (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    post_id UUID NOT NULL REFERENCES blog_posts(id) ON DELETE CASCADE,
    tag_id UUID NOT NULL REFERENCES blog_tags(id) ON DELETE CASCADE,
    
    -- Prevent duplicate associations
    UNIQUE(post_id, tag_id),
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Menu system for navigation
CREATE TABLE navigation_menus (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(100) UNIQUE NOT NULL, -- 'main', 'footer', 'mobile'
    description TEXT,
    
    -- Multilingual support
    display_name JSONB, -- {"nl": "Hoofdmenu", "en": "Main Menu"}
    
    -- Status
    active BOOLEAN DEFAULT true,
    
    -- Metadata
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Menu items
CREATE TABLE navigation_menu_items (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    menu_id UUID NOT NULL REFERENCES navigation_menus(id) ON DELETE CASCADE,
    
    -- Multilingual labels
    label JSONB NOT NULL, -- {"nl": "Over Mij", "en": "About"}
    
    -- Navigation
    url VARCHAR(500),
    route VARCHAR(255), -- Internal route like '/about'
    external_url BOOLEAN DEFAULT false,
    
    -- Hierarchy
    parent_id UUID REFERENCES navigation_menu_items(id) ON DELETE CASCADE,
    sort_order INTEGER DEFAULT 0,
    
    -- Styling & Behavior
    css_classes VARCHAR(255),
    icon VARCHAR(100), -- Icon name or SVG
    target VARCHAR(20) DEFAULT '_self', -- '_blank', '_self', etc.
    
    -- Visibility & Permissions
    visible BOOLEAN DEFAULT true,
    auth_required BOOLEAN DEFAULT false,
    roles TEXT[], -- Array of roles that can see this item
    
    -- Metadata
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Pages table for static content (About, Services, etc.)
CREATE TABLE pages (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    slug VARCHAR(255) UNIQUE NOT NULL,
    
    -- Multilingual content
    title JSONB NOT NULL,
    content JSONB NOT NULL,
    excerpt JSONB,
    
    -- SEO
    meta_title JSONB,
    meta_description JSONB,
    meta_keywords TEXT[],
    
    -- Media
    featured_image VARCHAR(500),
    
    -- Settings
    template VARCHAR(100) DEFAULT 'default',
    show_in_sitemap BOOLEAN DEFAULT true,
    
    -- Status
    published BOOLEAN DEFAULT true,
    
    -- Timestamps
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    published_at TIMESTAMP WITH TIME ZONE
);

-- Contact form submissions
CREATE TABLE contact_submissions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    
    -- Form data
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    company VARCHAR(255),
    subject VARCHAR(500),
    message TEXT NOT NULL,
    
    -- Metadata
    language VARCHAR(2) DEFAULT 'nl',
    user_agent TEXT,
    ip_address INET,
    referrer VARCHAR(500),
    
    -- Status
    status VARCHAR(20) DEFAULT 'new' CHECK (status IN ('new', 'read', 'replied', 'archived')),
    replied_at TIMESTAMP WITH TIME ZONE,
    
    -- Timestamps
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Analytics table for basic tracking
CREATE TABLE page_views (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    
    -- Page info
    url VARCHAR(500) NOT NULL,
    title VARCHAR(500),
    
    -- Visitor info (anonymized)
    visitor_hash VARCHAR(64), -- Hashed IP + User Agent
    country_code VARCHAR(2),
    language VARCHAR(10),
    
    -- Technical info
    user_agent TEXT,
    referrer VARCHAR(500),
    
    -- Timestamp
    viewed_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Indexes for performance

-- Users
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_role ON users(role);
CREATE INDEX idx_users_created_at ON users(created_at);

-- Blog posts
CREATE INDEX idx_blog_posts_slug ON blog_posts(slug);
CREATE INDEX idx_blog_posts_status ON blog_posts(status);
CREATE INDEX idx_blog_posts_published_at ON blog_posts(published_at DESC) WHERE status = 'published';
CREATE INDEX idx_blog_posts_author_id ON blog_posts(author_id);
CREATE INDEX idx_blog_posts_category_id ON blog_posts(category_id);
CREATE INDEX idx_blog_posts_created_at ON blog_posts(created_at DESC);

-- Full-text search indexes
CREATE INDEX idx_blog_posts_title_gin ON blog_posts USING GIN(title);
CREATE INDEX idx_blog_posts_content_gin ON blog_posts USING GIN(content);
CREATE INDEX idx_blog_posts_excerpt_gin ON blog_posts USING GIN(excerpt);

-- Categories
CREATE INDEX idx_blog_categories_slug ON blog_categories(slug);
CREATE INDEX idx_blog_categories_parent_id ON blog_categories(parent_id);
CREATE INDEX idx_blog_categories_sort_order ON blog_categories(sort_order);

-- Tags
CREATE INDEX idx_blog_tags_name ON blog_tags(name);
CREATE INDEX idx_blog_tags_slug ON blog_tags(slug);

-- Post-tags relationship
CREATE INDEX idx_blog_post_tags_post_id ON blog_post_tags(post_id);
CREATE INDEX idx_blog_post_tags_tag_id ON blog_post_tags(tag_id);

-- Navigation
CREATE INDEX idx_navigation_menu_items_menu_id ON navigation_menu_items(menu_id);
CREATE INDEX idx_navigation_menu_items_parent_id ON navigation_menu_items(parent_id);
CREATE INDEX idx_navigation_menu_items_sort_order ON navigation_menu_items(sort_order);

-- Pages
CREATE INDEX idx_pages_slug ON pages(slug);
CREATE INDEX idx_pages_published ON pages(published);

-- Analytics
CREATE INDEX idx_page_views_url ON page_views(url);
CREATE INDEX idx_page_views_viewed_at ON page_views(viewed_at DESC);

-- Functions for automatic updated_at
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Triggers for updated_at
CREATE TRIGGER update_users_updated_at BEFORE UPDATE ON users FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_blog_posts_updated_at BEFORE UPDATE ON blog_posts FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_blog_categories_updated_at BEFORE UPDATE ON blog_categories FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_blog_tags_updated_at BEFORE UPDATE ON blog_tags FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_pages_updated_at BEFORE UPDATE ON pages FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_navigation_menus_updated_at BEFORE UPDATE ON navigation_menus FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_navigation_menu_items_updated_at BEFORE UPDATE ON navigation_menu_items FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Function to update tag post count
CREATE OR REPLACE FUNCTION update_tag_post_count()
RETURNS TRIGGER AS $$
BEGIN
    IF TG_OP = 'DELETE' THEN
        UPDATE blog_tags SET post_count = (
            SELECT COUNT(*) FROM blog_post_tags WHERE tag_id = OLD.tag_id
        ) WHERE id = OLD.tag_id;
        RETURN OLD;
    ELSIF TG_OP = 'INSERT' THEN
        UPDATE blog_tags SET post_count = (
            SELECT COUNT(*) FROM blog_post_tags WHERE tag_id = NEW.tag_id
        ) WHERE id = NEW.tag_id;
        RETURN NEW;
    END IF;
    RETURN NULL;
END;
$$ language 'plpgsql';

-- Trigger for tag post count
CREATE TRIGGER update_tag_post_count_trigger 
    AFTER INSERT OR DELETE ON blog_post_tags 
    FOR EACH ROW EXECUTE FUNCTION update_tag_post_count();

-- Comments

-- This schema provides:
-- ✅ Multilingual content support (JSONB fields)
-- ✅ Blog system with categories, tags, authors
-- ✅ Flexible navigation/menu system
-- ✅ Static pages support
-- ✅ Contact form handling
-- ✅ Basic analytics
-- ✅ SEO optimization fields
-- ✅ AI translation tracking
-- ✅ Performance indexes
-- ✅ Automatic timestamp updates
-- ✅ Referential integrity
-- ✅ Proper data types and constraints