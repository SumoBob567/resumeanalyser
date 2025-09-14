import { useState } from "react";
import axios from "axios";

function App() {
  const [resumeFile, setResumeFile] = useState(null);
  const [jobText, setJobText] = useState("");
  const [result, setResult] = useState(null);
  
  const API_URL = process.env.REACT_APP_API_URL || "http://127.0.0.1:8000";

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

    try {
      //const res = await axios.post("http://127.0.0.1:8000/analyze", formData);
      const res = await axios.post(`${API_URL}/analyze`, formData);
      setResult(res.data);
    } catch (err) {
      console.error("Axios error:", err.response || err.message);
      alert("Error analyzing resume: " + (err.response?.status || err.message));
    }
  };

  const sortByImportance = (skills) => {
    const order = { high: 0, medium: 1, low: 2 };
    return [...skills].sort(
      (a, b) => (order[a.importance] ?? 3) - (order[b.importance] ?? 3)
    );
  };

  return (
    <div className="min-h-screen bg-gray-50 flex flex-col items-center p-6">
      <h1 className="text-3xl font-bold text-gray-800 mb-6">
        Resume Analyzer
      </h1>

      {/*Upload*/}
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

      {/*Results*/}
      {result && (
        <div className="mt-8 w-full max-w-2xl bg-white shadow-lg rounded-2xl p-6 space-y-6">
          <h2 className="text-xl font-bold mb-4 text-gray-800">Results</h2>

          {/*Score*/}
          <div>
            <p className="font-medium text-gray-700 mb-2">
              Semantic Match Score
            </p>
            <div className="w-full bg-gray-200 rounded-full h-4 overflow-hidden">
              <div
                className={`
                  h-4 rounded-full transition-all 
                  ${result.final_score >= 70 ? "bg-green-600" : result.final_score >= 55 ? "bg-amber-500" : "bg-red-600"}
                `}
                style={{ width: `${result.final_score.toFixed(0)}%` }}
              />
            </div>
            <p className="text-sm text-gray-600 mt-1">
              {result.final_score.toFixed(2) + "% - "}
              {result.final_score >= 70
                ? "You're good to go!"
                : result.final_score >= 55
                ? "Almost there!"
                : "Needs improvement"}
            </p>
          </div>

          {/*Matched*/}
          <div>
            <p className="font-medium text-gray-700 mb-2">Matched Skills</p>
            <div className="flex flex-wrap gap-2">
              {sortByImportance(result.matched_skills).length > 0 ? (
                sortByImportance(result.matched_skills).map((item, idx) => (
                  <span
                    key={idx}
                    className="bg-green-100 text-green-800 px-3 py-1 rounded-full text-sm"
                  >
                    {item.skill}
                  </span>
                ))
              ) : (
                <p className="text-gray-500 text-sm">No matched skills</p>
              )}
            </div>
          </div>

          {/*Missing*/}
          <div>
            <p className="font-medium text-gray-700 mb-2">Missing Skills</p>
            <div className="flex flex-wrap gap-2">
              {sortByImportance(result.missing_skills).length > 0 ? (
                sortByImportance(result.missing_skills).map((item, idx) => (
                  <span
                    key={idx}
                    className="bg-red-100 text-red-800 px-3 py-1 rounded-full text-sm"
                  >
                    {item.skill}
                  </span>
                ))
              ) : (
                <p className="text-gray-500 text-sm">No missing skills.</p>
              )}
            </div>
          </div>
          {/*Priorities*/}
          <div>
            <p className="font-medium text-gray-700 mb-2">
              Recommended Priorities
            </p>
              
            {(() => {
              const high = result.missing_skills.filter((s) => s.importance === "high");
              const medium = result.missing_skills.filter((s) => s.importance === "medium");
              const low = result.missing_skills.filter((s) => s.importance === "low");

              let priorities = [...high];

              if (priorities.length < 5) {
                const needed = 5 - priorities.length;
                priorities = [...priorities, ...medium.slice(0, needed)];
              }
              if (priorities.length < 5) {
                const needed = 5 - priorities.length;
                priorities = [...priorities, ...low.slice(0, needed)];
              }

              return (
                <ul className="list-disc list-inside text-gray-700 space-y-1">
                  {priorities.length > 0 ? (
                    priorities.map((item, idx) => (
                      <li
                        key={idx}
                        className={`${
                          item.importance === "high"
                            ? "font-bold text-red-700"
                            : item.importance === "medium"
                            ? "font-semibold text-yellow-700"
                            : "text-gray-600"
                        }`}
                      >
                        {item.skill + " (" + item.importance + ")"}
                      </li>
                    ))
                  ) : (
                    <li className="text-gray-500 text-sm">
                      No missing skills to prioritise.
                    </li>
                  )}
                </ul>
              );
            })()}
          </div>
        </div>
      )}
    </div>
  );
}

export default App;

