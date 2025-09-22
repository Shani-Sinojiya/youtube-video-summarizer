"use client";
import Link from "next/link";
import { motion } from "framer-motion";

export function CTASection() {
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

  const itemVariants = {
    hidden: { opacity: 0, y: 30 },
    visible: {
      opacity: 1,
      y: 0,
      transition: { duration: 0.6, ease: "easeOut" },
    },
  };

  const buttonVariants = {
    hidden: { opacity: 0, scale: 0.8 },
    visible: {
      opacity: 1,
      scale: 1,
      transition: { duration: 0.5, ease: "easeOut" },
    },
  };

  return (
    <section id="get-started" className="py-16 bg-blue-900 text-white">
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
        <motion.div
          variants={containerVariants}
          initial="hidden"
          whileInView="visible"
          viewport={{ once: true }}
        >
          <motion.h2
            variants={itemVariants}
            className="text-3xl font-bold mb-6"
          >
            Ready to Get Legal Help in Your Language?
          </motion.h2>

          <motion.p variants={itemVariants} className="text-blue-100 mb-8">
            Recapify is here to make Indian law accessible to everyone,
            regardless of education or tech skills.
          </motion.p>

          <motion.div
            variants={itemVariants}
            className="flex flex-col sm:flex-row justify-center gap-4 mb-10"
          >
            <motion.div variants={buttonVariants}>
              <Link
                href="/chat"
                className="bg-orange-500 hover:bg-orange-600 text-white px-8 py-4 rounded-full font-medium text-lg transition duration-300 flex items-center justify-center"
              >
                <motion.i
                  className="fas fa-comments mr-2"
                  whileHover={{ scale: 1.1 }}
                  transition={{ duration: 0.2 }}
                />
                Start Chatting Now
              </Link>
            </motion.div>

            <motion.div variants={buttonVariants}>
              <Link
                href="/voice"
                className="bg-white hover:bg-gray-100 text-blue-900 px-8 py-4 rounded-full font-medium text-lg transition duration-300 flex items-center justify-center voice-btn"
              >
                <motion.i
                  className="fas fa-microphone mr-2"
                  whileHover={{ scale: 1.1 }}
                  transition={{ duration: 0.2 }}
                />
                Speak to Recapify
              </Link>
            </motion.div>
          </motion.div>

          <motion.div variants={itemVariants} className="flex justify-center">
            <motion.div
              whileHover={{ scale: 1.05 }}
              transition={{ duration: 0.2 }}
            >
              <Link
                href="#"
                className="flex items-center text-blue-200 hover:text-white"
              >
                <motion.i
                  className="fab fa-whatsapp text-2xl mr-2"
                  whileHover={{ rotate: 10 }}
                  transition={{ duration: 0.2 }}
                />
                <span>Or message us on WhatsApp</span>
              </Link>
            </motion.div>
          </motion.div>
        </motion.div>
      </div>
    </section>
  );
}
