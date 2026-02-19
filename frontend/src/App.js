import { useState, useEffect, useCallback } from "react";
import axios from "axios";

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL || "http://localhost:8000";
const API = `${BACKEND_URL}/api`;

// ─── Icons (inline SVGs to avoid extra dependencies) ─────────────────
const Icons = {
  Search: () => (
    <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><circle cx="11" cy="11" r="8"/><path d="m21 21-4.3-4.3"/></svg>
  ),
  Briefcase: () => (
    <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><rect width="20" height="14" x="2" y="7" rx="2" ry="2"/><path d="M16 21V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v16"/></svg>
  ),
  Target: () => (
    <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><circle cx="12" cy="12" r="10"/><circle cx="12" cy="12" r="6"/><circle cx="12" cy="12" r="2"/></svg>
  ),
  TrendingUp: () => (
    <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><polyline points="22 7 13.5 15.5 8.5 10.5 2 17"/><polyline points="16 7 22 7 22 13"/></svg>
  ),
  FileText: () => (
    <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M14.5 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7.5L14.5 2z"/><polyline points="14 2 14 8 20 8"/><line x1="16" x2="8" y1="13" y2="13"/><line x1="16" x2="8" y1="17" y2="17"/><line x1="10" x2="8" y1="9" y2="9"/></svg>
  ),
  Globe: () => (
    <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><circle cx="12" cy="12" r="10"/><line x1="2" x2="22" y1="12" y2="12"/><path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"/></svg>
  ),
  ExternalLink: () => (
    <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"/><polyline points="15 3 21 3 21 9"/><line x1="10" x2="21" y1="14" y2="3"/></svg>
  ),
  X: () => (
    <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M18 6 6 18"/><path d="m6 6 12 12"/></svg>
  ),
  Loader: () => (
    <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="animate-spin"><path d="M21 12a9 9 0 1 1-6.219-8.56"/></svg>
  ),
  Rocket: () => (
    <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M4.5 16.5c-1.5 1.26-2 5-2 5s3.74-.5 5-2c.71-.84.7-2.13-.09-2.91a2.18 2.18 0 0 0-2.91-.09z"/><path d="m12 15-3-3a22 22 0 0 1 2-3.95A12.88 12.88 0 0 1 22 2c0 2.72-.78 7.5-6 11a22.35 22.35 0 0 1-4 2z"/><path d="M9 12H4s.55-3.03 2-4c1.62-1.08 5 0 5 0"/><path d="M12 15v5s3.03-.55 4-2c1.08-1.62 0-5 0-5"/></svg>
  ),
  Clock: () => (
    <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>
  ),
  MapPin: () => (
    <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0Z"/><circle cx="12" cy="10" r="3"/></svg>
  ),
  Building: () => (
    <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><rect width="16" height="20" x="4" y="2" rx="2" ry="2"/><path d="M9 22v-4h6v4"/><path d="M8 6h.01"/><path d="M16 6h.01"/><path d="M12 6h.01"/><path d="M12 10h.01"/><path d="M12 14h.01"/><path d="M16 10h.01"/><path d="M16 14h.01"/><path d="M8 10h.01"/><path d="M8 14h.01"/></svg>
  ),
  Zap: () => (
    <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/></svg>
  ),
};

// ─── Match Badge Component ───────────────────────────────────────────
const MatchBadge = ({ percentage }) => {
  let colorClass = "badge-low";
  if (percentage >= 80) colorClass = "badge-high";
  else if (percentage >= 60) colorClass = "badge-medium";

  return (
    <span className={`match-badge ${colorClass}`}>
      {percentage.toFixed(0)}% Match
    </span>
  );
};

// ─── Stat Card Component ─────────────────────────────────────────────
const StatCard = ({ icon, label, value, gradient, delay }) => (
  <div className={`stat-card ${gradient}`} style={{ animationDelay: `${delay}ms` }}>
    <div className="stat-card-icon">{icon}</div>
    <div className="stat-card-content">
      <p className="stat-card-value">{value}</p>
      <p className="stat-card-label">{label}</p>
    </div>
  </div>
);

// ─── Job Card Component ──────────────────────────────────────────────
const JobCard = ({ job, onViewCoverLetter, delay }) => (
  <div className="job-card" style={{ animationDelay: `${delay}ms` }}>
    <div className="job-card-header">
      <div className="job-card-title-section">
        <h3 className="job-card-title">{job.title || "Untitled Position"}</h3>
        <div className="job-card-meta">
          <span className="job-card-meta-item">
            <Icons.Building /> {job.company || "Unknown Company"}
          </span>
          <span className="job-card-meta-item">
            <Icons.MapPin /> {job.location || "Remote"}
          </span>
          <span className="job-card-meta-item">
            <Icons.Globe /> {job.portal || "Unknown"}
          </span>
        </div>
      </div>
      <MatchBadge percentage={job.match_percentage || 0} />
    </div>

    {job.matched_skills && job.matched_skills.length > 0 && (
      <div className="job-card-skills">
        <span className="skills-label">Matched Skills:</span>
        <div className="skills-tags">
          {job.matched_skills.map((skill, i) => (
            <span key={i} className="skill-tag matched">{skill}</span>
          ))}
        </div>
      </div>
    )}

    {job.missing_skills && job.missing_skills.length > 0 && (
      <div className="job-card-skills">
        <span className="skills-label">To Learn:</span>
        <div className="skills-tags">
          {job.missing_skills.slice(0, 3).map((skill, i) => (
            <span key={i} className="skill-tag missing">{skill}</span>
          ))}
          {job.missing_skills.length > 3 && (
            <span className="skill-tag more">+{job.missing_skills.length - 3} more</span>
          )}
        </div>
      </div>
    )}

    <div className="job-card-footer">
      <div className="job-card-date">
        <Icons.Clock />
        {job.date_found ? new Date(job.date_found).toLocaleDateString() : "Recent"}
      </div>
      <div className="job-card-actions">
        {job.cover_letter_generated === "Yes" && (
          <button
            className="btn btn-ghost btn-sm"
            onClick={() => onViewCoverLetter(job)}
          >
            <Icons.FileText /> Cover Letter
          </button>
        )}
        {job.link && (
          <a
            href={job.link}
            target="_blank"
            rel="noopener noreferrer"
            className="btn btn-primary btn-sm"
          >
            Apply <Icons.ExternalLink />
          </a>
        )}
      </div>
    </div>
  </div>
);

// ─── Cover Letter Modal ──────────────────────────────────────────────
const CoverLetterModal = ({ isOpen, onClose, job, content }) => {
  if (!isOpen) return null;

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-content" onClick={(e) => e.stopPropagation()}>
        <div className="modal-header">
          <div>
            <h2 className="modal-title">Cover Letter</h2>
            <p className="modal-subtitle">
              {job?.title} at {job?.company}
            </p>
          </div>
          <button className="btn btn-ghost btn-icon" onClick={onClose}>
            <Icons.X />
          </button>
        </div>
        <div className="modal-body">
          <pre className="cover-letter-content">{content || "No cover letter available."}</pre>
        </div>
        <div className="modal-footer">
          <button className="btn btn-ghost" onClick={onClose}>
            Close
          </button>
          <button
            className="btn btn-primary"
            onClick={() => {
              navigator.clipboard.writeText(content || "");
              alert("Cover letter copied to clipboard!");
            }}
          >
            Copy to Clipboard
          </button>
        </div>
      </div>
    </div>
  );
};

// ─── Empty State Component ───────────────────────────────────────────
const EmptyState = ({ onSearch, isSearching }) => (
  <div className="empty-state">
    <div className="empty-state-icon">
      <Icons.Rocket />
    </div>
    <h3>No Jobs Found Yet</h3>
    <p>
      Start your first job search to discover opportunities matching your skills.
      The assistant will scrape multiple job portals and find the best matches.
    </p>
    <button
      className="btn btn-primary btn-lg"
      onClick={onSearch}
      disabled={isSearching}
    >
      {isSearching ? (
        <>
          <Icons.Loader /> Searching...
        </>
      ) : (
        <>
          <Icons.Search /> Start Job Search
        </>
      )}
    </button>
  </div>
);

// ─── Main App Component ──────────────────────────────────────────────
function App() {
  const [jobs, setJobs] = useState([]);
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);
  const [searching, setSearching] = useState(false);
  const [searchQuery, setSearchQuery] = useState("");
  const [sortBy, setSortBy] = useState("match");
  const [filterPortal, setFilterPortal] = useState("all");
  const [coverLetterModal, setCoverLetterModal] = useState({
    isOpen: false,
    job: null,
    content: "",
  });
  const [backendStatus, setBackendStatus] = useState("checking");
  const [activeTab, setActiveTab] = useState("dashboard");

  // Fetch data from API
  const fetchData = useCallback(async () => {
    try {
      const [jobsRes, statsRes] = await Promise.all([
        axios.get(`${API}/jobs`).catch(() => ({ data: [] })),
        axios.get(`${API}/stats`).catch(() => ({ data: null })),
      ]);

      setJobs(jobsRes.data || []);
      setStats(statsRes.data);
      setBackendStatus("connected");
    } catch (err) {
      console.error("Failed to fetch data:", err);
      setBackendStatus("disconnected");
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchData();
    // Poll every 30 seconds
    const interval = setInterval(fetchData, 30000);
    return () => clearInterval(interval);
  }, [fetchData]);

  // Trigger job search
  const handleSearch = async () => {
    setSearching(true);
    try {
      await axios.post(`${API}/search`, { task: "morning" });
      // Wait a bit then refresh
      setTimeout(() => {
        fetchData();
        setSearching(false);
      }, 5000);
    } catch (err) {
      console.error("Search failed:", err);
      setSearching(false);
      alert("Failed to trigger search. Is the backend running?");
    }
  };

  // View cover letter
  const handleViewCoverLetter = async (job) => {
    const filename = job.cover_letter_path
      ? job.cover_letter_path.split(/[/\\]/).pop()
      : "";
    let content = "";

    if (filename) {
      try {
        const res = await axios.get(`${API}/cover-letters/${filename}`);
        content = res.data.content;
      } catch {
        content = "Could not load cover letter.";
      }
    }

    setCoverLetterModal({ isOpen: true, job, content });
  };

  // Filter and sort jobs
  const filteredJobs = jobs
    .filter((job) => {
      const matchesSearch =
        !searchQuery ||
        job.title?.toLowerCase().includes(searchQuery.toLowerCase()) ||
        job.company?.toLowerCase().includes(searchQuery.toLowerCase()) ||
        job.portal?.toLowerCase().includes(searchQuery.toLowerCase());
      const matchesPortal =
        filterPortal === "all" || job.portal === filterPortal;
      return matchesSearch && matchesPortal;
    })
    .sort((a, b) => {
      if (sortBy === "match")
        return (b.match_percentage || 0) - (a.match_percentage || 0);
      if (sortBy === "date")
        return new Date(b.date_found || 0) - new Date(a.date_found || 0);
      if (sortBy === "company")
        return (a.company || "").localeCompare(b.company || "");
      return 0;
    });

  // Get unique portals for filter
  const portals = [...new Set(jobs.map((j) => j.portal).filter(Boolean))];

  if (loading) {
    return (
      <div className="app-loading">
        <div className="loading-spinner">
          <Icons.Loader />
        </div>
        <p>Loading AI Job Assistant...</p>
      </div>
    );
  }

  return (
    <div className="app">
      {/* ─── Header ────────────────────────────────────────────── */}
      <header className="app-header">
        <div className="header-left">
          <div className="logo">
            <Icons.Zap />
          </div>
          <div>
            <h1 className="header-title">AI Job Assistant</h1>
            <p className="header-subtitle">Smart Job Search & Application Tracker</p>
          </div>
        </div>
        <div className="header-right">
          <div className={`connection-status ${backendStatus}`}>
            <span className="status-dot" />
            {backendStatus === "connected" ? "API Connected" : "API Disconnected"}
          </div>
          <button
            id="search-trigger"
            className="btn btn-primary"
            onClick={handleSearch}
            disabled={searching}
          >
            {searching ? (
              <>
                <Icons.Loader /> Searching...
              </>
            ) : (
              <>
                <Icons.Search /> New Search
              </>
            )}
          </button>
        </div>
      </header>

      {/* ─── Navigation Tabs ───────────────────────────────────── */}
      <nav className="tab-nav">
        <button
          className={`tab-btn ${activeTab === "dashboard" ? "active" : ""}`}
          onClick={() => setActiveTab("dashboard")}
        >
          Dashboard
        </button>
        <button
          className={`tab-btn ${activeTab === "jobs" ? "active" : ""}`}
          onClick={() => setActiveTab("jobs")}
        >
          Job Listings ({jobs.length})
        </button>
      </nav>

      <main className="app-main">
        {/* ─── Dashboard Tab ─────────────────────────────────────── */}
        {activeTab === "dashboard" && (
          <div className="dashboard">
            {/* Stats Cards */}
            <div className="stats-grid">
              <StatCard
                icon={<Icons.Briefcase />}
                label="Total Jobs Found"
                value={stats?.total_jobs_found || jobs.length || 0}
                gradient="gradient-blue"
                delay={0}
              />
              <StatCard
                icon={<Icons.Target />}
                label="Matched Jobs"
                value={stats?.matched_jobs || filteredJobs.length || 0}
                gradient="gradient-purple"
                delay={100}
              />
              <StatCard
                icon={<Icons.TrendingUp />}
                label="Highest Match"
                value={`${(stats?.highest_match || 0).toFixed(0)}%`}
                gradient="gradient-green"
                delay={200}
              />
              <StatCard
                icon={<Icons.Globe />}
                label="Portals Scraped"
                value={stats?.portals_scraped || portals.length || 0}
                gradient="gradient-orange"
                delay={300}
              />
              <StatCard
                icon={<Icons.FileText />}
                label="Cover Letters"
                value={stats?.cover_letters_generated || 0}
                gradient="gradient-pink"
                delay={400}
              />
              <StatCard
                icon={<Icons.Clock />}
                label="Last Run"
                value={
                  stats?.last_run && stats.last_run !== "Never"
                    ? new Date(stats.last_run).toLocaleDateString()
                    : "Never"
                }
                gradient="gradient-teal"
                delay={500}
              />
            </div>

            {/* Quick Actions */}
            <div className="section">
              <h2 className="section-title">Quick Actions</h2>
              <div className="quick-actions">
                <button
                  className="action-card"
                  onClick={handleSearch}
                  disabled={searching}
                >
                  <Icons.Search />
                  <span>Run Job Search</span>
                  <small>Scrape all portals for new jobs</small>
                </button>
                <button
                  className="action-card"
                  onClick={() => setActiveTab("jobs")}
                >
                  <Icons.Briefcase />
                  <span>View All Jobs</span>
                  <small>Browse and filter matched jobs</small>
                </button>
                <a
                  className="action-card"
                  href={`${BACKEND_URL}/docs`}
                  target="_blank"
                  rel="noopener noreferrer"
                >
                  <Icons.FileText />
                  <span>API Docs</span>
                  <small>Interactive Swagger documentation</small>
                </a>
              </div>
            </div>

            {/* Recent Jobs Preview */}
            {jobs.length > 0 && (
              <div className="section">
                <div className="section-header">
                  <h2 className="section-title">Recent Matches</h2>
                  <button
                    className="btn btn-ghost btn-sm"
                    onClick={() => setActiveTab("jobs")}
                  >
                    View All →
                  </button>
                </div>
                <div className="jobs-grid">
                  {filteredJobs.slice(0, 4).map((job, i) => (
                    <JobCard
                      key={job.job_id || i}
                      job={job}
                      onViewCoverLetter={handleViewCoverLetter}
                      delay={i * 100}
                    />
                  ))}
                </div>
              </div>
            )}

            {jobs.length === 0 && (
              <EmptyState onSearch={handleSearch} isSearching={searching} />
            )}
          </div>
        )}

        {/* ─── Jobs Tab ──────────────────────────────────────────── */}
        {activeTab === "jobs" && (
          <div className="jobs-view">
            {/* Search & Filter Bar */}
            <div className="filter-bar">
              <div className="search-input-wrapper">
                <Icons.Search />
                <input
                  id="job-search-input"
                  type="text"
                  placeholder="Search jobs by title, company, or portal..."
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  className="search-input"
                />
              </div>
              <div className="filter-controls">
                <select
                  id="sort-select"
                  value={sortBy}
                  onChange={(e) => setSortBy(e.target.value)}
                  className="filter-select"
                >
                  <option value="match">Sort by Match %</option>
                  <option value="date">Sort by Date</option>
                  <option value="company">Sort by Company</option>
                </select>
                <select
                  id="portal-filter"
                  value={filterPortal}
                  onChange={(e) => setFilterPortal(e.target.value)}
                  className="filter-select"
                >
                  <option value="all">All Portals</option>
                  {portals.map((p) => (
                    <option key={p} value={p}>
                      {p}
                    </option>
                  ))}
                </select>
              </div>
            </div>

            {/* Results Count */}
            <div className="results-count">
              Showing {filteredJobs.length} of {jobs.length} jobs
            </div>

            {/* Job Cards Grid */}
            {filteredJobs.length > 0 ? (
              <div className="jobs-list">
                {filteredJobs.map((job, i) => (
                  <JobCard
                    key={job.job_id || i}
                    job={job}
                    onViewCoverLetter={handleViewCoverLetter}
                    delay={i * 50}
                  />
                ))}
              </div>
            ) : (
              <EmptyState onSearch={handleSearch} isSearching={searching} />
            )}
          </div>
        )}
      </main>

      {/* ─── Footer ────────────────────────────────────────────── */}
      <footer className="app-footer">
        <p>
          AI Job Assistant • Built with FastAPI + React •{" "}
          <a
            href="https://github.com/PranayaKD/AI-Assistant"
            target="_blank"
            rel="noopener noreferrer"
          >
            GitHub
          </a>
        </p>
      </footer>

      {/* ─── Cover Letter Modal ────────────────────────────────── */}
      <CoverLetterModal
        isOpen={coverLetterModal.isOpen}
        onClose={() =>
          setCoverLetterModal({ isOpen: false, job: null, content: "" })
        }
        job={coverLetterModal.job}
        content={coverLetterModal.content}
      />
    </div>
  );
}

export default App;
