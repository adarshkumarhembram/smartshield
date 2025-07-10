// src/components/ResultCard.jsx

const ResultCard = ({ result }) => {
  const { fraud, confidence } = result;

  return (
    <div
      className={`mt-6 p-4 rounded shadow text-white font-semibold ${
        fraud ? "bg-red-600" : "bg-green-600"
      }`}
    >
      {fraud ? "⚠️ Fraudulent Transaction Detected!" : "✅ Transaction is Safe"}
      <p className="mt-1">Confidence Score: {confidence * 100}%</p>
    </div>
  );
};

export default ResultCard;
