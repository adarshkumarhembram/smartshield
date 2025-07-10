import PredictForm from "./pages/PredictForm";
import History from "./pages/History";

function App() {
  return (
    <div className="bg-gray-100 min-h-screen p-4">
      <h1 className="text-3xl font-bold text-center text-blue-700 mb-6">
        💳 SmartShield – Fraud Detection System
      </h1>
      <PredictForm />
      <History />
    </div>
  );
}

export default App;
