import { useEffect, useState } from "react";

import {
  ArrowLeft,
  CheckCircle,
  CreditCard,
  Crown,
  ShieldCheck,
  Sparkles,
} from "lucide-react";

import { useNavigate } from "react-router-dom";

import API from "../api/axios";

export default function Billing() {

  const navigate = useNavigate();

  const [loading, setLoading] =
    useState(false);

  const [subscription, setSubscription] =
    useState(null);

  const [provider, setProvider] =
    useState("razorpay");

  const plans = [
    {
      name: "Basic",
      amount: 0,
      price: "₹0",
      color: "from-slate-500 to-slate-700",
      icon: ShieldCheck,
      features: [
        "5 Team Members",
        "500 Credits",
        "Basic Analytics",
        "Email Support",
      ],
    },

    {
      name: "Silver",
      amount: 1499,
      price: "₹1499",
      color: "from-indigo-500 to-blue-600",
      icon: Sparkles,
      features: [
        "20 Team Members",
        "1000 Credits",
        "Advanced Analytics",
        "Priority Support",
      ],
    },

    {
      name: "Gold",
      amount: 4999,
      price: "₹4999",
      color: "from-yellow-400 to-orange-500",
      icon: Crown,
      popular: true,
      features: [
        "Unlimited Members",
        "10000 Credits",
        "AI Insights",
        "Dedicated Support",
      ],
    },
  ];

  // =====================================
  // LOAD SUBSCRIPTION
  // =====================================
  const loadSubscription = async () => {

    try {

      const { data } =
        await API.get(
          "/payments/subscription"
        );

      setSubscription(data);

    } catch (error) {

      console.log(error);

      setSubscription(null);
    }
  };

  useEffect(() => {
    API.get("/payments/subscription")
      .then(({ data }) => setSubscription(data))
      .catch((error) => {
        console.log(error);
        setSubscription(null);
      });
  }, []);

  // =====================================
// HANDLE PAYMENT
// =====================================
const handlePayment = async (plan) => {

  try {

    setLoading(true);

    // =================================
    // FREE BASIC PLAN
    // =================================
    if (plan.toLowerCase() === "basic") {

      const { data } =
        await API.post(
          "/payments/create-payment",
          {
            plan: "basic",
            provider: "free",
          }
        );

      await loadSubscription();

      alert(
        data.message ||
        "Basic Plan Activated"
      );

      return;
    }

    // =================================
    // PAID PLANS
    // =================================
    const { data } =
      await API.post(
        "/payments/create-payment",
        {
          plan: plan.toLowerCase(),
          provider,
        }
      );

    // =================================
    // STRIPE
    // =================================
    if (provider === "stripe") {

      globalThis.location.assign(
        data.checkout_url
      );

      return;
    }

    // =================================
    // RAZORPAY
    // =================================
    if (provider === "razorpay") {

      const options = {

        key: data.key,

        amount: data.amount,

        currency: data.currency,

        name: "TaskFlow",

        description:
          `${plan} Subscription`,

        order_id:
          data.order_id || data.id,

        method: {
          upi: true,
          card: true,
          netbanking: true,
          wallet: true,
          paylater: true,
        },

        handler: async function (
          response
        ) {

          try {

            await API.post(
              "/payments/verify",
              {
                razorpay_order_id:
                  response.razorpay_order_id,

                razorpay_payment_id:
                  response.razorpay_payment_id,

                razorpay_signature:
                  response.razorpay_signature,

                plan:
                  plan.toLowerCase(),
              }
            );

            await loadSubscription();

            alert(
              `${plan} Plan Activated`
            );

          } catch (error) {

            console.log(error);

            alert(
              "Payment Verification Failed"
            );
          }
        },

        prefill: {
          name: "Test User",
          email: "test@example.com",
          contact: "9999999999",
        },

        theme: {
          color: "#4f46e5",
        },
      };

      const razorpay =
        new window.Razorpay(options);

      razorpay.on(
        "payment.failed",
        function (response) {

          console.log(
            response.error
          );

          alert("Payment Failed");
        }
      );

      razorpay.open();
    }

  } catch (error) {

    console.log(error);

    alert(
      "Unable to Process Payment"
    );

  } finally {

    setLoading(false);
  }
};

  // =====================================
  // PLAN INFO
  // =====================================
  const planTitle =
    subscription?.plan
      ? `${subscription.plan[0].toUpperCase()}${subscription.plan.slice(1)} Plan`
      : "No Active Plan";

  const statusText =
    subscription?.status === "active"
      ? "Subscription Active"
      : "Subscription Inactive";

  // =====================================
  // UI
  // =====================================
  return (

    <div className="min-h-screen bg-gradient-to-br from-slate-950 via-indigo-950 to-slate-950 px-4 py-5 font-[Inter]">

      {/* BACK BUTTON */}
      <div className="mb-5">

        <button
          onClick={() =>
            navigate("/dashboard")
          }
          className="flex items-center gap-2 px-3 py-1.5 rounded-lg bg-white/10 hover:bg-white/20 transition-all text-white text-sm border border-white/10"
        >

          <ArrowLeft size={16} />

          Back to Dashboard

        </button>
      </div>

      {/* HEADER */}
      <div className="text-center mb-8">

        <h1 className="text-3xl md:text-4xl font-bold text-white mb-2 tracking-tight">

          Billing & Plans

        </h1>

        <p className="text-indigo-200 text-sm md:text-base">

          Upgrade your workspace
          with enterprise-grade
          features

        </p>
      </div>

      {/* PROVIDER SELECTOR */}
      <div className="flex justify-center gap-2 mb-6">

        <button
          onClick={() =>
            setProvider("razorpay")
          }
          className={`px-4 py-1.5 rounded-lg text-sm font-medium transition-all ${
            provider === "razorpay"
              ? "bg-blue-600 text-white"
              : "bg-white/10 text-white border border-white/10"
          }`}
        >
          Razorpay
        </button>

        <button
          onClick={() =>
            setProvider("stripe")
          }
          className={`px-4 py-1.5 rounded-lg text-sm font-medium transition-all ${
            provider === "stripe"
              ? "bg-indigo-600 text-white"
              : "bg-white/10 text-white border border-white/10"
          }`}
        >
          Stripe
        </button>

      </div>

      {/* SUBSCRIPTION CARD */}
      <div className="max-w-4xl mx-auto mb-6">

        <div className="bg-white/10 backdrop-blur-lg border border-white/10 rounded-2xl p-4 flex flex-col md:flex-row justify-between items-center shadow-xl">

          <div>

            <p className="text-indigo-300 text-xs mb-1">

              Current Plan

            </p>

            <h2 className="text-xl font-semibold text-white">

              {planTitle}

            </h2>

            <p className="text-indigo-200 mt-1 text-sm">

              {subscription
                ? `${subscription.credits} Credits Remaining`
                : "500 Credits Remaining"}

            </p>

          </div>

          <div className="mt-4 md:mt-0 flex items-center gap-2 bg-emerald-500/20 border border-emerald-400/30 px-3 py-2 rounded-xl">

            <CheckCircle
              className="text-emerald-400"
              size={18}
            />

            <span className="text-emerald-300 text-sm font-medium">

              {statusText}

            </span>

          </div>
        </div>
      </div>

      {/* PLANS */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-5 max-w-6xl mx-auto">

        {plans.map((plan) => {

          const Icon = plan.icon;

          return (

            <div
              key={plan.name}
              className="relative rounded-2xl overflow-hidden border border-white/10 bg-white/10 backdrop-blur-xl shadow-xl hover:scale-[1.02] transition-all duration-300"
            >

              {/* POPULAR */}
              {plan.popular && (

                <div className="absolute top-3 right-3 bg-gradient-to-r from-yellow-400 to-orange-500 text-black text-[10px] font-bold px-2 py-1 rounded-full">

                  POPULAR

                </div>
              )}

              {/* HEADER */}
              <div
                className={`bg-gradient-to-r ${plan.color} p-4 text-white`}
              >

                <div className="flex items-center gap-2 mb-3">

                  <div className="bg-white/20 p-2 rounded-xl">

                    <Icon size={22} />

                  </div>

                  <h2 className="text-xl font-semibold">

                    {plan.name}

                  </h2>

                </div>

                <h3 className="text-3xl font-bold">

                  {plan.price}

                </h3>

                <p className="mt-1 text-xs text-white/80">

                  Per Month

                </p>

              </div>

              {/* BODY */}
              <div className="p-4">

                <div className="space-y-2 mb-5">

                  {plan.features.map(
                    (feature) => (

                    <div
                      key={feature}
                      className="flex items-center gap-2 text-indigo-100 text-sm"
                    >

                      <CheckCircle
                        size={15}
                        className="text-emerald-400"
                      />

                      {feature}

                    </div>
                  ))}
                </div>

                {/* BUTTON */}
                <button
                  disabled={loading}
                  onClick={() =>
                    handlePayment(plan.name)
                  }
                  className={`w-full py-2.5 rounded-xl text-sm font-semibold text-white bg-gradient-to-r ${plan.color} hover:opacity-90 transition-all flex items-center justify-center gap-2`}
                >

                  <CreditCard size={18} />

                  {loading
                    ? "Processing..."
                    : `Choose ${plan.name}`}

                </button>

              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
