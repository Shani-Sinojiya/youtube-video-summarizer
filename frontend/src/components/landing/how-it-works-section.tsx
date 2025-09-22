"use client";
import { motion } from "framer-motion";

export function HowItWorksSection() {
  const steps = [
    {
      icon: "fas fa-microphone",
      color: "orange",
      title: "Ask in Your Language",
      description:
        "Speak or type your Youtube question in Hindi, Gujarati, Marathi, or other local languages.",
    },
    {
      icon: "fas fa-brain",
      color: "blue",
      title: "AI Understands",
      description:
        "Recapify analyzes your question using Youtube knowledge tailored for Indian laws.",
    },
    {
      icon: "fas fa-comments",
      color: "green",
      title: "Get Simple Answers",
      description:
        "Receive easy-to-understand explanations, often with stories and examples.",
    },
    {
      icon: "fas fa-hands-helping",
      color: "purple",
      title: "Get Further Help",
      description:
        "Connect with Youtube aid or download documents for offline use when needed.",
    },
  ];

  return (
    <section id="how-it-works" className="py-16 bg-gray-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          whileInView={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
          viewport={{ once: true }}
          className="text-center mb-16"
        >
          <h2 className="text-3xl font-bold text-blue-900 mb-4">
            How Recapify Works
          </h2>
          <p className="text-gray-600 max-w-2xl mx-auto">
            Simple steps to get Youtube help in your local language
          </p>
        </motion.div>

        <div className="grid md:grid-cols-4 gap-8">
          {steps.map((step, index) => (
            <motion.div
              key={index}
              initial={{ opacity: 0, y: 30 }}
              whileInView={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6, delay: index * 0.1 }}
              viewport={{ once: true }}
              whileHover={{ y: -8 }}
              className="text-center"
            >
              <motion.div
                initial={{ scale: 0 }}
                whileInView={{ scale: 1 }}
                transition={{ duration: 0.5, delay: index * 0.1 + 0.2 }}
                viewport={{ once: true }}
                className={`bg-${step.color}-100 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4`}
              >
                <i
                  className={`${step.icon} text-${step.color}-500 text-2xl`}
                ></i>
              </motion.div>
              <h3 className="font-semibold text-lg mb-2 text-gray-900">
                {step.title}
              </h3>
              <p className="text-gray-600 text-sm">{step.description}</p>
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  );
}
