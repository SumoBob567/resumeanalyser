import { useState } from "react";
import axios from "axios";

function App() {
  const [resumeFile, setResumeFile] = useState(null);
  const [jobText, setJobText] = useState("");
  const [result, setResult] = useState(null);

  const handleFileChange = (e) => {
    setResumeFile(e.target.files[0]);
  };

  const handleSubmit = async () => {
    if (!resumeFile || !jobText) {
      alert("Please upload a resume and paste job description.");
      return;
    }

    const formData = new FormData();
    formData.append("resume", resumeFile);
    formData.append("job_text", jobText);

    for (let [key, value] of formData.entries()) {
    console.log(key, value);
    }

    try {
      const res = await axios.post("http://127.0.0.1:8000/analyze", formData);
      setResult(res.data);
    } catch (err) {
      console.error("Axios error:", err.response || err.message);
      alert("Error analyzing resume: " + (err.response?.status || err.message));
    }
  };

  return (
    
    <div className="min-h-screen bg-gray-50 flex flex-col items-center p-6">
      {"Hello"}
      <h1 className="text-3xl font-bold text-gray-800 mb-6">
        Resume Analyzer
      </h1>

      {/* Upload Card */}
      <div className="bg-white shadow-xl rounded-2xl p-6 w-full max-w-2xl space-y-4">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Upload Resume (PDF or DOCX)
          </label>
          <input
            type="file"
            accept=".pdf,.docx"
            onChange={handleFileChange}
            className="block w-full text-sm text-gray-700 border border-gray-300 rounded-lg cursor-pointer bg-gray-50"
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Paste Job Description
          </label>
          <textarea
            value={jobText}
            onChange={(e) => setJobText(e.target.value)}
            rows="6"
            className="w-full p-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:outline-none"
          />
        </div>

        <button
          onClick={handleSubmit}
          className="w-full bg-blue-600 hover:bg-blue-700 text-white font-semibold py-2 px-4 rounded-lg transition"
        >
          Analyze Resume
        </button>
      </div>

      {/* Results */}
      {result && (
        <div className="mt-8 w-full max-w-2xl bg-white shadow-lg rounded-2xl p-6 space-y-4">
          <h2 className="text-xl font-bold mb-4 text-gray-800">Results</h2>

          {/* SBERT Score */}
          <div>
            <p className="font-medium text-gray-700 mb-2">Semantic Match Score</p>
            <div className="w-full bg-gray-200 rounded-full h-4 overflow-hidden">
              <div
                className="bg-blue-600 h-4 rounded-full transition-all"
                style={{ width: `${result.sbert_score.toFixed(0)}%` }}
              />
            </div>
            <p className="text-sm text-gray-600 mt-1">
              {result.sbert_score.toFixed(2)}%
            </p>
          </div>

          {/* Matched Skills */}
          <div>
            <p className="font-medium text-gray-700 mb-2">Matched Skills</p>
            <div className="flex flex-wrap gap-2">
              {result.matched_skills.length > 0 ? (
                result.matched_skills.map((skill, idx) => (
                  <span
                    key={idx}
                    className="bg-green-100 text-green-800 px-3 py-1 rounded-full text-sm"
                  >
                    {skill}
                  </span>
                ))
              ) : (
                <p className="text-gray-500 text-sm">No matched skills</p>
              )}
            </div>
          </div>

          {/* Missing Skills */}
          <div>
            <p className="font-medium text-gray-700 mb-2">Missing Skills</p>
            <div className="flex flex-wrap gap-2">
              {result.missing_skills.length > 0 ? (
                result.missing_skills.map((skill, idx) => (
                  <span
                    key={idx}
                    className="bg-red-100 text-red-800 px-3 py-1 rounded-full text-sm"
                  >
                    {skill}
                  </span>
                ))
              ) : (
                <p className="text-gray-500 text-sm">No missing skills 🎉</p>
              )}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default App;
