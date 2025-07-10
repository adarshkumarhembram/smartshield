import { useEffect, useState } from "react";
import axios from "axios";

const History = () => {
  const [transactions, setTransactions] = useState([]);

  useEffect(() => {
    axios.get("http://localhost:5000/transactions").then((res) => {
      setTransactions(res.data);
    });
  }, []);

  return (
    <div className="max-w-5xl mx-auto mt-10">
      <h2 className="text-xl font-bold mb-4">🗃️ Recent Predictions</h2>
      <table className="w-full table-auto border">
        <thead>
          <tr className="bg-blue-100">
            <th>#</th>
            <th>Fraud</th>
            <th>Confidence</th>
            <th>Time</th>
          </tr>
        </thead>
        <tbody>
          {transactions.map((txn, i) => (
            <tr key={txn._id} className="text-center border-t">
              <td>{i + 1}</td>
              <td>{txn.prediction ? "⚠️ Fraud" : "✅ Safe"}</td>
              <td>{(txn.confidence * 100).toFixed(2)}%</td>
              <td>{txn.timestamp}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default History;
