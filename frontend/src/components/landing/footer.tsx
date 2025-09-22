"use client";
import Link from "next/link";
import { motion } from "framer-motion";

export function Footer() {
  const containerVariants = {
    hidden: { opacity: 0 },
    visible: {
      opacity: 1,
      transition: {
        staggerChildren: 0.1,
        delayChildren: 0.2,
      },
    },
  };

  const itemVariants = {
    hidden: { opacity: 0, y: 20 },
    visible: {
      opacity: 1,
      y: 0,
      transition: { duration: 0.5 },
    },
  };

  const socialIconVariants = {
    hidden: { opacity: 0, scale: 0 },
    visible: {
      opacity: 1,
      scale: 1,
      transition: { duration: 0.3 },
    },
    hover: {
      scale: 1.2,
      transition: { duration: 0.2 },
    },
  };

  return (
    <footer className="bg-gray-900 text-white py-12">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <motion.div
          variants={containerVariants}
          initial="hidden"
          whileInView="visible"
          viewport={{ once: true }}
          className="grid grid-cols-2 md:grid-cols-4 gap-8 mb-8"
        >
          <motion.div variants={itemVariants}>
            <h3 className="text-lg font-semibold mb-4">Recapify</h3>
            <p className="text-gray-400 text-sm">
              Your AI-powered Youtube friend making Indian law accessible in
              local languages.
            </p>
          </motion.div>

          <motion.div variants={itemVariants}>
            <h3 className="text-lg font-semibold mb-4">Quick Links</h3>
            <ul className="space-y-2">
              {[
                { href: "/", text: "Home" },
                { href: "#features", text: "Features" },
                { href: "#how-it-works", text: "How It Works" },
                { href: "#faq", text: "FAQ" },
              ].map((link, index) => (
                <motion.li
                  key={link.text}
                  initial={{ opacity: 0, x: -10 }}
                  whileInView={{ opacity: 1, x: 0 }}
                  transition={{ delay: index * 0.1, duration: 0.3 }}
                  viewport={{ once: true }}
                >
                  <Link
                    href={link.href}
                    className="text-gray-400 hover:text-white text-sm transition-colors duration-200"
                  >
                    {link.text}
                  </Link>
                </motion.li>
              ))}
            </ul>
          </motion.div>

          <motion.div variants={itemVariants}>
            <h3 className="text-lg font-semibold mb-4">Legal</h3>
            <ul className="space-y-2">
              {[
                { href: "/privacy-policy", text: "Privacy Policy" },
                { href: "/terms-of-service", text: "Terms of Service" },
                { href: "/disclaimer", text: "Disclaimer" },
              ].map((link, index) => (
                <motion.li
                  key={link.text}
                  initial={{ opacity: 0, x: -10 }}
                  whileInView={{ opacity: 1, x: 0 }}
                  transition={{ delay: index * 0.1, duration: 0.3 }}
                  viewport={{ once: true }}
                >
                  <Link
                    href={link.href}
                    className="text-gray-400 hover:text-white text-sm transition-colors duration-200"
                  >
                    {link.text}
                  </Link>
                </motion.li>
              ))}
            </ul>
          </motion.div>

          <motion.div variants={itemVariants}>
            <h3 className="text-lg font-semibold mb-4">Connect With Us</h3>
            <div className="flex space-x-4 mb-4">
              {[
                "facebook-f",
                "twitter",
                "instagram",
                "linkedin-in",
                "whatsapp",
              ].map((platform, index) => (
                <motion.a
                  key={platform}
                  href="#"
                  variants={socialIconVariants}
                  whileHover="hover"
                  className="text-gray-400 hover:text-white transition-colors duration-200"
                >
                  <i className={`fab fa-${platform}`}></i>
                </motion.a>
              ))}
            </div>
            <motion.p
              initial={{ opacity: 0 }}
              whileInView={{ opacity: 1 }}
              transition={{ delay: 0.3, duration: 0.5 }}
              viewport={{ once: true }}
              className="text-gray-400 text-sm"
            >
              Email: help@nyayamitra.org
            </motion.p>
            <motion.p
              initial={{ opacity: 0 }}
              whileInView={{ opacity: 1 }}
              transition={{ delay: 0.4, duration: 0.5 }}
              viewport={{ once: true }}
              className="text-gray-400 text-sm"
            >
              Toll-free: 1800-123-4567
            </motion.p>
          </motion.div>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.3 }}
          viewport={{ once: true }}
          className="border-t border-gray-800 pt-8"
        >
          <div className="flex flex-col md:flex-row justify-between items-center">
            <motion.p
              initial={{ opacity: 0, x: -20 }}
              whileInView={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.5, delay: 0.4 }}
              viewport={{ once: true }}
              className="text-gray-400 text-sm mb-4 md:mb-0 flex items-center"
            >
              &copy; {new Date().getFullYear()} Recapify. All rights reserved.
            </motion.p>
            <motion.div
              initial={{ opacity: 0, x: 20 }}
              whileInView={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.5, delay: 0.5 }}
              viewport={{ once: true }}
              className="flex items-center space-x-6"
            >
              <p className="text-gray-400 text-sm">Supported by:</p>
              <div className="flex space-x-4">
                {["NGO", "Gov"].map((supporter, index) => (
                  <motion.div
                    key={supporter}
                    initial={{ opacity: 0, scale: 0 }}
                    whileInView={{ opacity: 1, scale: 1 }}
                    whileHover={{ scale: 1.1 }}
                    transition={{ delay: 0.6 + index * 0.1, duration: 0.3 }}
                    viewport={{ once: true }}
                    className="bg-white w-10 h-10 rounded flex items-center justify-center text-gray-800 font-bold text-xs cursor-pointer"
                  >
                    {supporter}
                  </motion.div>
                ))}
              </div>
            </motion.div>
          </div>
        </motion.div>
      </div>
    </footer>
  );
}
