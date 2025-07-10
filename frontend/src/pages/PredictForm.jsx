import { useState } from "react";
import axios from "axios";
import ResultCard from "../components/ResultCard";

const PredictForm = () => {
  const [features, setFeatures] = useState(Array(30).fill(""));
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleChange = (index, value) => {
    const updated = [...features];
    updated[index] = value;
    setFeatures(updated);
  };

  const autofill = () => {
    const sample = Array(30)
      .fill()
      .map(() => (Math.random() * 4 - 2).toFixed(4)); // Random between -2 to +2
    setFeatures(sample);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (features.some((f) => f === "")) {
      alert("❗ Please fill all 30 features.");
      return;
    }

    setLoading(true);
    try {
      const res = await axios.post("http://localhost:5000/predict", {
        features: features.map(Number),
      });
      setResult(res.data);
    } catch (err) {
      console.error(err);
      alert("❌ Prediction failed. Check backend.");
    }
    setLoading(false);
  };

  return (
    <div className="max-w-4xl mx-auto p-4">
      <h2 className="text-2xl font-bold mb-4 text-blue-700">
        🔍 Credit Card Fraud Prediction
      </h2>
      <form onSubmit={handleSubmit} className="grid grid-cols-2 md:grid-cols-4 gap-3">
        {features.map((val, index) => (
          <input
            key={index}
            type="number"
            step="any"
            placeholder={`V${index + 1}`}
            className="p-2 border rounded"
            value={val}
            onChange={(e) => handleChange(index, e.target.value)}
          />
        ))}

        <button
          type="button"
          onClick={autofill}
          className="col-span-full bg-gray-400 text-white py-2 rounded hover:bg-gray-500"
        >
          Autofill Sample Data
        </button>

        <button
          type="submit"
          className="col-span-full bg-blue-600 text-white py-2 rounded hover:bg-blue-700"
        >
          {loading ? "Predicting..." : "Predict"}
        </button>
      </form>

      {result && <ResultCard result={result} />}
    </div>
  );
};

export default PredictForm;
