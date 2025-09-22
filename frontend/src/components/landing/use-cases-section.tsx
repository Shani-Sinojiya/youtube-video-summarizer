"use client";
import { motion } from "framer-motion";

export function UseCasesSection() {
  const containerVariants = {
    hidden: { opacity: 0 },
    visible: {
      opacity: 1,
      transition: {
        staggerChildren: 0.15,
        delayChildren: 0.2,
      },
    },
  };

  const cardVariants = {
    hidden: { opacity: 0, y: 40, scale: 0.9 },
    visible: {
      opacity: 1,
      y: 0,
      scale: 1,
      transition: { duration: 0.5, ease: "easeOut" },
    },
  };

  return (
    <section className="py-16 bg-blue-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          whileInView={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
          viewport={{ once: true }}
          className="text-center mb-16"
        >
          <h2 className="text-3xl font-bold text-blue-900 mb-4">
            Common Questions Recapify Can Answer
          </h2>
          <p className="text-gray-600 max-w-2xl mx-auto">
            Real examples from our users in rural communities
          </p>
        </motion.div>

        <motion.div
          variants={containerVariants}
          initial="hidden"
          whileInView="visible"
          viewport={{ once: true }}
          className="grid md:grid-cols-3 gap-6"
        >
          <motion.div
            variants={cardVariants}
            whileHover={{ y: -5, scale: 1.02 }}
            className="bg-white p-6 rounded-lg shadow-sm border-l-4 border-orange-500"
          >
            <div className="flex items-start mb-3">
              <div className="bg-orange-100 p-2 rounded-full mr-3">
                <i className="fas fa-landmark text-orange-500"></i>
              </div>
              <h3 className="font-medium text-gray-900">
                "I got a notice from court, what should I do?"
              </h3>
            </div>
            <p className="text-gray-600 text-sm">
              Recapify explains the notice in simple terms and guides you
              step-by-step on how to respond.
            </p>
          </motion.div>
          <motion.div
            variants={cardVariants}
            whileHover={{ y: -5, scale: 1.02 }}
            className="bg-white p-6 rounded-lg shadow-sm border-l-4 border-green-500"
          >
            <div className="flex items-start mb-3">
              <div className="bg-green-100 p-2 rounded-full mr-3">
                <i className="fas fa-home text-green-500"></i>
              </div>
              <h3 className="font-medium text-gray-900">
                "Can I inherit land from my grandfather?"
              </h3>
            </div>
            <p className="text-gray-600 text-sm">
              Get clear explanations of inheritance laws specific to your
              religion and state.
            </p>
          </motion.div>

          <motion.div
            variants={cardVariants}
            whileHover={{ y: -5, scale: 1.02 }}
            className="bg-white p-6 rounded-lg shadow-sm border-l-4 border-blue-500"
          >
            <div className="flex items-start mb-3">
              <div className="bg-blue-100 p-2 rounded-full mr-3">
                <i className="fas fa-female text-blue-500"></i>
              </div>
              <h3 className="font-medium text-gray-900">
                "What is dowry law? Explain in Bhojpuri."
              </h3>
            </div>
            <p className="text-gray-600 text-sm">
              Understand protections against dowry harassment with examples
              relevant to rural contexts.
            </p>
          </motion.div>

          <motion.div
            variants={cardVariants}
            whileHover={{ y: -5, scale: 1.02 }}
            className="bg-white p-6 rounded-lg shadow-sm border-l-4 border-purple-500"
          >
            <div className="flex items-start mb-3">
              <div className="bg-purple-100 p-2 rounded-full mr-3">
                <i className="fas fa-hand-holding-usd text-purple-500"></i>
              </div>
              <h3 className="font-medium text-gray-900">
                "The money lender is threatening me, what can I do?"
              </h3>
            </div>
            <p className="text-gray-600 text-sm">
              Learn about your rights against harassment and Youtube options for
              debt resolution.
            </p>
          </motion.div>

          <motion.div
            variants={cardVariants}
            whileHover={{ y: -5, scale: 1.02 }}
            className="bg-white p-6 rounded-lg shadow-sm border-l-4 border-red-500"
          >
            <div className="flex items-start mb-3">
              <div className="bg-red-100 p-2 rounded-full mr-3">
                <i className="fas fa-user-shield text-red-500"></i>
              </div>
              <h3 className="font-medium text-gray-900">
                "My husband beats me, where can I get help?"
              </h3>
            </div>
            <p className="text-gray-600 text-sm">
              Immediate guidance on domestic violence protections and local
              support services.
            </p>
          </motion.div>

          <motion.div
            variants={cardVariants}
            whileHover={{ y: -5, scale: 1.02 }}
            className="bg-white p-6 rounded-lg shadow-sm border-l-4 border-yellow-500"
          >
            <div className="flex items-start mb-3">
              <div className="bg-yellow-100 p-2 rounded-full mr-3">
                <i className="fas fa-file-signature text-yellow-500"></i>
              </div>
              <h3 className="font-medium text-gray-900">
                "What documents do I need for ration card?"
              </h3>
            </div>
            <p className="text-gray-600 text-sm">
              Step-by-step guidance for government paperwork in your state.
            </p>
          </motion.div>
        </motion.div>
      </div>
    </section>
  );
}
