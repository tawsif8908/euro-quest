// Frontend API Integration Example
// Add this to your HTML files to connect with the Django backend

// Base API URL - Django runs on port 8000
const API_BASE = 'http://localhost:8000/api';

// Example: Fetch and display jobs
async function loadJobs() {
  try {
    const response = await fetch(`${API_BASE}/jobs/`);
    const data = await response.json();

    if (response.ok) {
      displayJobs(data);
      return data;
    } else {
      console.error('Error loading jobs:', data);
      return null;
    }
  } catch (error) {
    console.error('Network error:', error);
    return null;
  }
}

// Example: Submit job application
async function submitApplication(jobId, applicationData) {
  try {
    const response = await fetch(`${API_BASE}/applications/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        job: jobId,
        ...applicationData
      })
    });

    const data = await response.json();

    if (response.ok) {
      alert('Application submitted successfully!');
      return data;
    } else {
      alert('Error: ' + JSON.stringify(data));
      return null;
    }
  } catch (error) {
    console.error('Network error:', error);
  }
}

// Example: Submit contact form
async function submitContact(contactData) {
  try {
    const response = await fetch(`${API_BASE}/contacts/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(contactData)
    });

    const data = await response.json();

    if (response.ok) {
      alert('Message sent successfully!');
      return data;
    } else {
      alert('Error: ' + JSON.stringify(data));
      return null;
    }
  } catch (error) {
    console.error('Network error:', error);
  }
}

// Example: Load blog posts
async function loadBlogPosts() {
  try {
    const response = await fetch(`${API_BASE}/blogs/`);
    const data = await response.json();

    if (response.ok) {
      displayBlogPosts(data);
    } else {
      console.error('Error loading blog posts:', data);
    }
  } catch (error) {
    console.error('Network error:', error);
  }
}

// Helper functions (implement these based on your UI)
function displayJobs(data) {
  // data is an array of job objects
  console.log('Jobs:', data);
  // Implement job display logic here
}

function displayBlogPosts(data) {
  // data is an array of blog post objects
  console.log('Blog posts:', data);
  // Implement blog display logic here
}

// Export functions for use in your HTML
window.API = {
  loadJobs,
  submitApplication,
  submitContact,
  loadBlogPosts
};