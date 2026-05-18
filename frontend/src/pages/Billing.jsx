import { useEffect, useState } from "react";

import {
  CheckCircle,
  CreditCard,
  Crown,
  ShieldCheck,
  Sparkles,
} from "lucide-react";

import API from "../api/axios";

export default function Billing() {
  const [loading, setLoading] = useState(false);
  const [subscription, setSubscription] = useState(null);

  const plans = [
    {
      name: "Basic",
      amount: 499,
      price: "₹499",
      color: "from-slate-500 to-slate-700",
      icon: ShieldCheck,
      features: ["5 Team Members", "100 Credits", "Basic Analytics", "Email Support"],
    },
    {
      name: "Silver",
      amount: 1499,
      price: "₹1499",
      color: "from-indigo-500 to-blue-600",
      icon: Sparkles,
      features: ["20 Team Members", "1000 Credits", "Advanced Analytics", "Priority Support"],
    },
    {
      name: "Gold",
      amount: 4999,
      price: "₹4999",
      color: "from-yellow-400 to-orange-500",
      icon: Crown,
      popular: true,
      features: ["Unlimited Members", "10000 Credits", "AI Insights", "Dedicated Support"],
    },
  ];

  const loadSubscription = async () => {
    const { data } = await API.get("/payments/subscription");
    setSubscription(data);
  };

  useEffect(() => {
    API.get("/payments/subscription")
      .then(({ data }) => setSubscription(data))
      .catch(() => setSubscription(null));
  }, []);

  const handlePayment = async (plan) => {
    try {
      setLoading(true);

      const { data } = await API.post("/payments/create-order", {
        plan: plan.toLowerCase(),
      });

      const options = {
        key: import.meta.env.VITE_RAZORPAY_KEY_ID,
        amount: data.amount,
        currency: data.currency,
        name: "TaskFlow",
        description: `${plan} Subscription`,
        order_id: data.id,
        handler: async function (response) {
          await API.post("/payments/verify", {
            ...response,
            plan: plan.toLowerCase(),
          });

          await loadSubscription();
          alert(`${plan} Plan Activated`);
        },
        theme: {
          color: "#4f46e5",
        },
      };

      const razorpay = new window.Razorpay(options);
      razorpay.open();
    } catch (error) {
      console.log(error);
      alert("Payment Failed");
    } finally {
      setLoading(false);
    }
  };

  const planTitle = subscription?.plan
    ? `${subscription.plan[0].toUpperCase()}${subscription.plan.slice(1)} Plan`
    : "No Active Plan";

  const statusText =
    subscription?.status === "active"
      ? "Subscription Active"
      : "Subscription Inactive";

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-950 via-indigo-950 to-slate-950 p-8">
      <div className="text-center mb-14">
        <h1 className="text-5xl font-extrabold text-white mb-4">Billing & Plans</h1>
        <p className="text-indigo-200 text-lg">
          Upgrade your workspace with enterprise-grade features
        </p>
      </div>

      <div className="max-w-5xl mx-auto mb-10">
        <div className="bg-white/10 backdrop-blur-lg border border-white/10 rounded-3xl p-6 flex flex-col md:flex-row justify-between items-center shadow-2xl">
          <div>
            <p className="text-indigo-300 text-sm mb-2">Current Plan</p>
            <h2 className="text-3xl font-bold text-white">{planTitle}</h2>
            <p className="text-indigo-200 mt-1">
              {subscription ? `${subscription.credits} Credits Remaining` : "0 Credits Remaining"}
            </p>
          </div>

          <div className="mt-5 md:mt-0 flex items-center gap-3 bg-emerald-500/20 border border-emerald-400/30 px-5 py-3 rounded-2xl">
            <CheckCircle className="text-emerald-400" size={22} />
            <span className="text-emerald-300 font-semibold">{statusText}</span>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-8 max-w-7xl mx-auto">
        {plans.map((plan) => {
          const Icon = plan.icon;

          return (
            <div
              key={plan.name}
              className="relative rounded-3xl overflow-hidden border border-white/10 bg-white/10 backdrop-blur-xl shadow-2xl hover:scale-105 transition-all duration-300"
            >
              {plan.popular && (
                <div className="absolute top-4 right-4 bg-gradient-to-r from-yellow-400 to-orange-500 text-black text-xs font-bold px-3 py-1 rounded-full">
                  MOST POPULAR
                </div>
              )}

              <div className={`bg-gradient-to-r ${plan.color} p-8 text-white`}>
                <div className="flex items-center gap-3 mb-5">
                  <div className="bg-white/20 p-3 rounded-2xl">
                    <Icon size={28} />
                  </div>
                  <h2 className="text-3xl font-bold">{plan.name}</h2>
                </div>

                <h3 className="text-5xl font-extrabold">{plan.price}</h3>
                <p className="mt-2 text-white/80">Per Month</p>
              </div>

              <div className="p-8">
                <div className="space-y-4 mb-8">
                  {plan.features.map((feature) => (
                    <div key={feature} className="flex items-center gap-3 text-indigo-100">
                      <CheckCircle size={18} className="text-emerald-400" />
                      {feature}
                    </div>
                  ))}
                </div>

                <button
                  disabled={loading}
                  onClick={() => handlePayment(plan.name)}
                  className={`w-full py-4 rounded-2xl font-bold text-white bg-gradient-to-r ${plan.color} hover:opacity-90 transition-all flex items-center justify-center gap-2`}
                >
                  <CreditCard size={20} />
                  {loading ? "Processing..." : `Choose ${plan.name}`}
                </button>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
