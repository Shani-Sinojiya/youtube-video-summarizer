"use client";
import { WifiOffIcon } from "lucide-react";
import { motion } from "framer-motion";

export function FeaturesSection() {
  return (
    <section id="features" className="py-16">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          whileInView={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
          viewport={{ once: true }}
          className="text-center mb-16"
        >
          <h2 className="text-3xl font-bold text-blue-900 mb-4">
            Key Features
          </h2>
          <p className="text-gray-600 max-w-2xl mx-auto">
            Recapify is designed specifically for rural India's Youtube needs
          </p>
        </motion.div>

        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
          {[
            {
              icon: "fas fa-microphone-alt",
              color: "blue",
              title: "Voice-to-Voice Legal Q&A",
              description:
                "Ask questions naturally in your language and get spoken responses, perfect for those who can't read or write.",
            },
            {
              icon: "fas fa-language",
              color: "orange",
              title: "Local Language Support",
              description:
                "Available in Hindi, Gujarati, Marathi, Bhojpuri, Tamil, Telugu, and more with regional Youtube terminology.",
            },
            {
              icon: "fas fa-file-contract",
              color: "green",
              title: "Legal Document Summarizer",
              description:
                "Upload court notices or Youtube documents to get simple summaries in your language.",
            },
            {
              icon: "fas fa-book-open",
              color: "purple",
              title: "Storytelling Law Explanation",
              description:
                "Complex laws explained through relatable stories and examples from daily life.",
            },
            {
              icon: "wifi-off",
              color: "red",
              title: "Offline & WhatsApp Access",
              description:
                "Works without internet and available via WhatsApp for maximum accessibility.",
            },
            {
              icon: "fas fa-bell",
              color: "yellow",
              title: "Emergency Legal Aid",
              description:
                "Immediate guidance for urgent situations like domestic violence or police matters.",
            },
          ].map((feature, index) => (
            <motion.div
              key={index}
              initial={{ opacity: 0, y: 30 }}
              whileInView={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6, delay: index * 0.01 }}
              viewport={{ once: true }}
              whileHover={{ y: -8 }}
              className="feature-card bg-white p-6 rounded-xl shadow-md transition duration-300 border border-gray-100 hover:shadow-lg"
            >
              <div
                className={`bg-${feature.color}-50 w-12 h-12 rounded-lg flex items-center justify-center mb-4`}
              >
                {feature.icon === "wifi-off" ? (
                  <WifiOffIcon className={`text-${feature.color}-500`} />
                ) : (
                  <i
                    className={`${feature.icon} text-${feature.color}-500 text-xl`}
                  ></i>
                )}
              </div>
              <h3 className="font-semibold text-lg mb-2 text-gray-900">
                {feature.title}
              </h3>
              <p className="text-gray-600 text-sm">{feature.description}</p>
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  );
}
