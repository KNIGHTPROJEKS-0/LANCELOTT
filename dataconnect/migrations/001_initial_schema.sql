-- LANCELOTT Security Framework - Database Schema
-- PostgreSQL migration script for Firebase Data Connect
-- Version: 1.0.0

-- Enable required extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- Create custom types (enums)
CREATE TYPE user_role AS ENUM ('ADMIN', 'SECURITY_ANALYST', 'PENETRATION_TESTER', 'VIEWER');
CREATE TYPE scan_type AS ENUM ('NETWORK_SCAN', 'WEB_SECURITY', 'OSINT_GATHERING', 'ASSET_DISCOVERY', 'SOCIAL_ENGINEERING', 'MOBILE_SECURITY', 'CLOUD_SECURITY', 'VULNERABILITY_SCAN', 'PENETRATION_TEST');
CREATE TYPE scan_status AS ENUM ('PENDING', 'RUNNING', 'COMPLETED', 'FAILED', 'CANCELLED', 'PAUSED');
CREATE TYPE vulnerability_severity AS ENUM ('CRITICAL', 'HIGH', 'MEDIUM', 'LOW', 'INFO');
CREATE TYPE vulnerability_status AS ENUM ('OPEN', 'CONFIRMED', 'FALSE_POSITIVE', 'FIXED', 'MITIGATED', 'ACCEPTED_RISK');
CREATE TYPE tool_category AS ENUM ('NETWORK_SCANNER', 'WEB_SECURITY', 'OSINT', 'VULNERABILITY_SCANNER', 'EXPLOITATION', 'FORENSICS', 'SOCIAL_ENGINEERING', 'MOBILE_SECURITY', 'CLOUD_SECURITY', 'AI_POWERED');
CREATE TYPE tool_status AS ENUM ('ACTIVE', 'INACTIVE', 'MAINTENANCE', 'ERROR', 'UPDATING');
CREATE TYPE execution_status AS ENUM ('QUEUED', 'RUNNING', 'COMPLETED', 'FAILED', 'TIMEOUT', 'CANCELLED');
CREATE TYPE report_type AS ENUM ('VULNERABILITY_REPORT', 'PENETRATION_TEST_REPORT', 'COMPLIANCE_REPORT', 'THREAT_ASSESSMENT', 'EXECUTIVE_SUMMARY', 'TECHNICAL_ANALYSIS', 'CUSTOM_REPORT');
CREATE TYPE report_format AS ENUM ('PDF', 'HTML', 'JSON', 'MARKDOWN', 'DOCX', 'CSV');
CREATE TYPE permission_type AS ENUM ('READ_SCANS', 'WRITE_SCANS', 'DELETE_SCANS', 'READ_REPORTS', 'WRITE_REPORTS', 'DELETE_REPORTS', 'MANAGE_TOOLS', 'ADMIN_ACCESS', 'AI_ANALYSIS', 'EXPORT_DATA');
CREATE TYPE setting_category AS ENUM ('SECURITY', 'PERFORMANCE', 'INTEGRATION', 'UI_UX', 'NOTIFICATIONS', 'AI_CONFIG', 'TOOL_CONFIG');
CREATE TYPE ai_analysis_type AS ENUM ('VULNERABILITY_ASSESSMENT', 'THREAT_INTELLIGENCE', 'RISK_ANALYSIS', 'ATTACK_PATH_ANALYSIS', 'REPORT_GENERATION', 'RECOMMENDATION_ENGINE', 'BEHAVIORAL_ANALYSIS');

-- Users table
CREATE TABLE users (
    user_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    display_name VARCHAR(255),
    role user_role NOT NULL DEFAULT 'VIEWER',
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    is_active BOOLEAN NOT NULL DEFAULT true,
    last_login_at TIMESTAMP WITH TIME ZONE,

    -- Indexes
    CONSTRAINT users_email_check CHECK (email ~* '^[A-Za-z0-9._%-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4}$')
);

-- Security tools table
CREATE TABLE security_tools (
    tool_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tool_name VARCHAR(100) UNIQUE NOT NULL,
    category tool_category NOT NULL,
    version VARCHAR(50),
    is_enabled BOOLEAN NOT NULL DEFAULT true,
    default_configuration JSONB,
    supported_targets TEXT[],
    status tool_status NOT NULL DEFAULT 'ACTIVE',
    last_health_check TIMESTAMP WITH TIME ZONE,
    description TEXT,
    documentation_url TEXT,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW()
);

-- Scans table
CREATE TABLE scans (
    scan_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    tool_name VARCHAR(100) NOT NULL,
    target VARCHAR(500) NOT NULL,
    scan_type scan_type NOT NULL,
    status scan_status NOT NULL DEFAULT 'PENDING',
    started_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    completed_at TIMESTAMP WITH TIME ZONE,
    duration_seconds INTEGER,
    configuration JSONB,
    results JSONB,
    metadata JSONB,
    error_message TEXT,

    -- Calculated duration trigger
    CONSTRAINT scans_duration_check CHECK (
        (completed_at IS NULL AND duration_seconds IS NULL) OR
        (completed_at IS NOT NULL AND duration_seconds IS NOT NULL)
    )
);

-- Vulnerabilities table
CREATE TABLE vulnerabilities (
    vulnerability_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    scan_id UUID NOT NULL REFERENCES scans(scan_id) ON DELETE CASCADE,
    cve_id VARCHAR(20),
    title VARCHAR(500) NOT NULL,
    description TEXT NOT NULL,
    severity vulnerability_severity NOT NULL,
    cvss_score DECIMAL(3,1) CHECK (cvss_score >= 0 AND cvss_score <= 10),
    affected_component VARCHAR(255),
    attack_vector VARCHAR(255),
    exploit_available BOOLEAN NOT NULL DEFAULT false,
    recommendation TEXT,
    status vulnerability_status NOT NULL DEFAULT 'OPEN',
    discovered_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    confirmed_at TIMESTAMP WITH TIME ZONE,
    resolved_at TIMESTAMP WITH TIME ZONE
);

-- AI Analysis table
CREATE TABLE ai_analysis (
    analysis_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    scan_id UUID REFERENCES scans(scan_id) ON DELETE CASCADE,
    user_id UUID NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    analysis_type ai_analysis_type NOT NULL,
    ai_provider VARCHAR(50) NOT NULL,
    model VARCHAR(100) NOT NULL,
    input_data JSONB NOT NULL,
    analysis_output JSONB,
    confidence_score DECIMAL(5,4) CHECK (confidence_score >= 0 AND confidence_score <= 1),
    tokens_used INTEGER,
    processing_time_ms INTEGER,
    estimated_cost DECIMAL(10,6),
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    completed_at TIMESTAMP WITH TIME ZONE
);

-- Tool Executions table
CREATE TABLE tool_executions (
    execution_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tool_id UUID NOT NULL REFERENCES security_tools(tool_id) ON DELETE CASCADE,
    user_id UUID NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    scan_id UUID REFERENCES scans(scan_id) ON DELETE CASCADE,
    command VARCHAR(1000) NOT NULL,
    arguments JSONB,
    environment JSONB,
    status execution_status NOT NULL DEFAULT 'QUEUED',
    started_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    completed_at TIMESTAMP WITH TIME ZONE,
    duration_ms INTEGER,
    stdout TEXT,
    stderr TEXT,
    exit_code INTEGER
);

-- Reports table
CREATE TABLE reports (
    report_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    title VARCHAR(255) NOT NULL,
    report_type report_type NOT NULL,
    format report_format NOT NULL,
    content JSONB NOT NULL,
    executive_summary TEXT,
    tags TEXT[],
    is_public BOOLEAN NOT NULL DEFAULT false,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    file_url TEXT,
    file_size_bytes BIGINT
);

-- API Keys table
CREATE TABLE api_keys (
    key_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    key_name VARCHAR(100) NOT NULL,
    key_hash VARCHAR(255) NOT NULL,
    permissions permission_type[],
    scope VARCHAR(255),
    is_active BOOLEAN NOT NULL DEFAULT true,
    expires_at TIMESTAMP WITH TIME ZONE,
    last_used_at TIMESTAMP WITH TIME ZONE,
    usage_count INTEGER NOT NULL DEFAULT 0,
    rate_limit_per_hour INTEGER DEFAULT 1000,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),

    UNIQUE(user_id, key_name)
);

-- System Settings table
CREATE TABLE system_settings (
    setting_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    setting_key VARCHAR(100) UNIQUE NOT NULL,
    setting_value JSONB NOT NULL,
    description TEXT,
    category setting_category NOT NULL,
    is_public BOOLEAN NOT NULL DEFAULT false,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    updated_by UUID REFERENCES users(user_id)
);

-- Audit Logs table
CREATE TABLE audit_logs (
    log_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(user_id) ON DELETE SET NULL,
    action VARCHAR(100) NOT NULL,
    resource VARCHAR(100) NOT NULL,
    resource_id UUID,
    details JSONB,
    ip_address INET,
    user_agent TEXT,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW()
);

-- Junction table for reports and scans many-to-many relationship
CREATE TABLE report_scans (
    report_id UUID NOT NULL REFERENCES reports(report_id) ON DELETE CASCADE,
    scan_id UUID NOT NULL REFERENCES scans(scan_id) ON DELETE CASCADE,
    PRIMARY KEY (report_id, scan_id)
);

-- Create indexes for performance
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_role ON users(role);
CREATE INDEX idx_users_active ON users(is_active);

CREATE INDEX idx_scans_user_id ON scans(user_id);
CREATE INDEX idx_scans_status ON scans(status);
CREATE INDEX idx_scans_started_at ON scans(started_at);
CREATE INDEX idx_scans_tool_name ON scans(tool_name);
CREATE INDEX idx_scans_scan_type ON scans(scan_type);

CREATE INDEX idx_vulnerabilities_scan_id ON vulnerabilities(scan_id);
CREATE INDEX idx_vulnerabilities_severity ON vulnerabilities(severity);
CREATE INDEX idx_vulnerabilities_status ON vulnerabilities(status);
CREATE INDEX idx_vulnerabilities_cve_id ON vulnerabilities(cve_id);
CREATE INDEX idx_vulnerabilities_discovered_at ON vulnerabilities(discovered_at);

CREATE INDEX idx_ai_analysis_user_id ON ai_analysis(user_id);
CREATE INDEX idx_ai_analysis_scan_id ON ai_analysis(scan_id);
CREATE INDEX idx_ai_analysis_type ON ai_analysis(analysis_type);
CREATE INDEX idx_ai_analysis_provider ON ai_analysis(ai_provider);
CREATE INDEX idx_ai_analysis_created_at ON ai_analysis(created_at);

CREATE INDEX idx_tool_executions_tool_id ON tool_executions(tool_id);
CREATE INDEX idx_tool_executions_user_id ON tool_executions(user_id);
CREATE INDEX idx_tool_executions_status ON tool_executions(status);
CREATE INDEX idx_tool_executions_started_at ON tool_executions(started_at);

CREATE INDEX idx_reports_user_id ON reports(user_id);
CREATE INDEX idx_reports_type ON reports(report_type);
CREATE INDEX idx_reports_created_at ON reports(created_at);
CREATE INDEX idx_reports_tags ON reports USING GIN(tags);

CREATE INDEX idx_api_keys_user_id ON api_keys(user_id);
CREATE INDEX idx_api_keys_active ON api_keys(is_active);
CREATE INDEX idx_api_keys_hash ON api_keys(key_hash);

CREATE INDEX idx_audit_logs_user_id ON audit_logs(user_id);
CREATE INDEX idx_audit_logs_action ON audit_logs(action);
CREATE INDEX idx_audit_logs_resource ON audit_logs(resource);
CREATE INDEX idx_audit_logs_created_at ON audit_logs(created_at);

-- Create triggers for updated_at timestamps
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_users_updated_at BEFORE UPDATE ON users FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_security_tools_updated_at BEFORE UPDATE ON security_tools FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_reports_updated_at BEFORE UPDATE ON reports FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_system_settings_updated_at BEFORE UPDATE ON system_settings FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Insert default security tools
INSERT INTO security_tools (tool_name, category, description, is_enabled) VALUES
('nmap', 'NETWORK_SCANNER', 'Network Mapper - Network discovery and security auditing', true),
('argus', 'NETWORK_SCANNER', 'Network monitoring and flow analysis tool', true),
('kraken', 'WEB_SECURITY', 'Multi-protocol brute force tool', true),
('metabigor', 'OSINT', 'Advanced OSINT framework for reconnaissance', true),
('dismap', 'NETWORK_SCANNER', 'Asset discovery and mapping tool', true),
('osmedeus', 'OSINT', 'Automated reconnaissance framework', true),
('spiderfoot', 'OSINT', 'Open source intelligence automation tool', true),
('social-analyzer', 'OSINT', 'Social media analysis and profiling tool', true),
('storm-breaker', 'SOCIAL_ENGINEERING', 'Social engineering toolkit', true),
('phonesploit-pro', 'MOBILE_SECURITY', 'Android device exploitation framework', true),
('redteam-toolkit', 'EXPLOITATION', 'Red team operations platform', true),
('vajra', 'CLOUD_SECURITY', 'Cloud security testing framework', true),
('web-check', 'WEB_SECURITY', 'Comprehensive web analysis tool', true),
('feroxbuster', 'WEB_SECURITY', 'Web content discovery tool', true),
('thc-hydra', 'EXPLOITATION', 'Network logon cracker', true),
('sherlock', 'OSINT', 'Username hunting across social networks', true),
('ui-tars', 'AI_POWERED', 'AI-powered testing automation framework', true);

-- Insert default system settings
INSERT INTO system_settings (setting_key, setting_value, description, category, is_public) VALUES
('max_concurrent_scans', '5', 'Maximum number of concurrent scans per user', 'PERFORMANCE', true),
('scan_timeout_minutes', '60', 'Default scan timeout in minutes', 'PERFORMANCE', true),
('enable_ai_analysis', 'true', 'Enable AI-powered analysis features', 'AI_CONFIG', true),
('default_ai_provider', '"openai"', 'Default AI provider for analysis', 'AI_CONFIG', false),
('vulnerability_retention_days', '365', 'Days to retain vulnerability data', 'SECURITY', true),
('audit_log_retention_days', '90', 'Days to retain audit logs', 'SECURITY', true);

-- Create views for common queries
CREATE VIEW user_scan_summary AS
SELECT
    u.user_id,
    u.email,
    u.display_name,
    COUNT(s.scan_id) as total_scans,
    COUNT(CASE WHEN s.status = 'COMPLETED' THEN 1 END) as completed_scans,
    COUNT(CASE WHEN s.status = 'FAILED' THEN 1 END) as failed_scans,
    COUNT(DISTINCT v.vulnerability_id) as total_vulnerabilities,
    COUNT(CASE WHEN v.severity = 'CRITICAL' THEN 1 END) as critical_vulnerabilities,
    MAX(s.started_at) as last_scan_date
FROM users u
LEFT JOIN scans s ON u.user_id = s.user_id
LEFT JOIN vulnerabilities v ON s.scan_id = v.scan_id
WHERE u.is_active = true
GROUP BY u.user_id, u.email, u.display_name;

CREATE VIEW vulnerability_summary AS
SELECT
    s.user_id,
    v.severity,
    v.status,
    COUNT(*) as vulnerability_count,
    AVG(v.cvss_score) as avg_cvss_score,
    MIN(v.discovered_at) as first_discovered,
    MAX(v.discovered_at) as last_discovered
FROM vulnerabilities v
JOIN scans s ON v.scan_id = s.scan_id
GROUP BY s.user_id, v.severity, v.status;

-- Grant permissions (adjust as needed for your environment)
-- Note: These would be set based on your specific user roles and security requirements
COMMENT ON DATABASE lancelott_db IS 'LANCELOTT Security Framework Database - Firebase Data Connect Backend';

-- Database schema version tracking
CREATE TABLE schema_versions (
    version VARCHAR(10) PRIMARY KEY,
    applied_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    description TEXT
);

INSERT INTO schema_versions (version, description) VALUES
('1.0.0', 'Initial LANCELOTT schema with core security framework tables');
