import { CheckCircle } from "lucide-react";

import { Link } from "react-router-dom";

export default function PaymentSuccess() {

  return (

    <div className="min-h-screen bg-slate-950 flex items-center justify-center px-4">

      <div className="bg-white/10 border border-white/10 backdrop-blur-xl rounded-2xl p-8 text-center max-w-md w-full">

        <div className="flex justify-center mb-4">

          <CheckCircle
            className="text-emerald-400"
            size={70}
          />

        </div>

        <h1 className="text-3xl font-bold text-white mb-3">

          Payment Successful

        </h1>

        <p className="text-slate-300 mb-6">

          Your subscription has been activated successfully.

        </p>

        <Link
          to="/billing"
          className="inline-block bg-indigo-600 hover:bg-indigo-700 transition-all px-5 py-2 rounded-xl text-white font-medium"
        >

          Back to Billing

        </Link>

      </div>
    </div>
  );
}