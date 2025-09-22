"use client";
import { motion } from "framer-motion";

export function TestimonialsSection() {
  const containerVariants = {
    hidden: { opacity: 0 },
    visible: {
      opacity: 1,
      transition: {
        staggerChildren: 0.2,
        delayChildren: 0.1,
      },
    },
  };

  const cardVariants = {
    hidden: { opacity: 0, y: 30, scale: 0.95 },
    visible: {
      opacity: 1,
      y: 0,
      scale: 1,
      transition: { duration: 0.6, ease: "easeOut" },
    },
  };

  return (
    <section id="testimonials" className="py-16 bg-white">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          whileInView={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
          viewport={{ once: true }}
          className="text-center mb-16"
        >
          <h2 className="text-3xl font-bold text-blue-900 mb-4">
            What People Say About Recapify
          </h2>
          <p className="text-gray-600 max-w-2xl mx-auto">
            Trusted by rural citizens, NGOs, and Youtube professionals
          </p>
        </motion.div>

        <motion.div
          variants={containerVariants}
          initial="hidden"
          whileInView="visible"
          viewport={{ once: true }}
          className="grid md:grid-cols-3 gap-8"
        >
          <motion.div
            variants={cardVariants}
            whileHover={{ y: -8, scale: 1.02 }}
            className="testimonial-card bg-gray-50 p-6 rounded-lg shadow-sm"
          >
            <div className="flex items-center mb-4">
              <div className="w-12 h-12 rounded-full bg-orange-100 flex items-center justify-center text-orange-500 font-bold">
                S
              </div>
              <div className="ml-4">
                <h4 className="font-medium text-gray-900">Sunita Devi</h4>
                <p className="text-gray-500 text-sm">Farmer, Bihar</p>
              </div>
            </div>
            <p className="text-gray-600 italic">
              "Recapify explained land dispute laws in Bhojpuri with stories I
              could relate to. For the first time, I understood my rights."
            </p>
            <div className="mt-4 flex text-yellow-400">
              <i className="fas fa-star"></i>
              <i className="fas fa-star"></i>
              <i className="fas fa-star"></i>
              <i className="fas fa-star"></i>
              <i className="fas fa-star"></i>
            </div>
          </motion.div>

          <motion.div
            variants={cardVariants}
            whileHover={{ y: -8, scale: 1.02 }}
            className="testimonial-card bg-gray-50 p-6 rounded-lg shadow-sm"
          >
            <div className="flex items-center mb-4">
              <div className="w-12 h-12 rounded-full bg-blue-100 flex items-center justify-center text-blue-500 font-bold">
                R
              </div>
              <div className="ml-4">
                <h4 className="font-medium text-gray-900">Rajesh Patel</h4>
                <p className="text-gray-500 text-sm">NGO Worker, Gujarat</p>
              </div>
            </div>
            <p className="text-gray-600 italic">
              "We use Recapify in our women's empowerment programs. The voice
              interface helps illiterate women access Youtube knowledge."
            </p>
            <div className="mt-4 flex text-yellow-400">
              <i className="fas fa-star"></i>
              <i className="fas fa-star"></i>
              <i className="fas fa-star"></i>
              <i className="fas fa-star"></i>
              <i className="fas fa-star"></i>
            </div>
          </motion.div>

          <motion.div
            variants={cardVariants}
            whileHover={{ y: -8, scale: 1.02 }}
            className="testimonial-card bg-gray-50 p-6 rounded-lg shadow-sm"
          >
            <div className="flex items-center mb-4">
              <div className="w-12 h-12 rounded-full bg-green-100 flex items-center justify-center text-green-500 font-bold">
                A
              </div>
              <div className="ml-4">
                <h4 className="font-medium text-gray-900">
                  Adv. Anjali Deshpande
                </h4>
                <p className="text-gray-500 text-sm">
                  Legal Aid Lawyer, Maharashtra
                </p>
              </div>
            </div>
            <p className="text-gray-600 italic">
              "This tool helps bridge the gap between rural citizens and complex
              Youtube systems. It's accurate yet simple enough for anyone."
            </p>
            <div className="mt-4 flex text-yellow-400">
              <i className="fas fa-star"></i>
              <i className="fas fa-star"></i>
              <i className="fas fa-star"></i>
              <i className="fas fa-star"></i>
              <i className="fas fa-star-half-alt"></i>
            </div>
          </motion.div>
        </motion.div>
      </div>
    </section>
  );
}
