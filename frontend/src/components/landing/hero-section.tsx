"use client";

import { motion } from "framer-motion";
import Link from "next/link";

export function HeroSection() {
  return (
    <section
      className="py-12 md:py-20"
      style={{
        background:
          "linear-gradient(135deg, rgba(255,153,51,0.1) 0%, rgba(255,255,255,1) 50%, rgba(19,136,8,0.1) 100%)",
      }}
    >
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="md:flex items-center">
          <motion.div
            initial={{ opacity: 0, x: -50 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.6 }}
            className="md:w-1/2 mb-10 md:mb-0"
          >
            <motion.h1
              initial={{ opacity: 0, y: 30 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6, delay: 0.2 }}
              className="text-4xl md:text-5xl font-bold text-blue-900 leading-tight mb-4"
            >
              Your AI Legal Friend in Your Language –{" "}
              <span className="text-orange-500">Recapify</span>
            </motion.h1>
            <motion.p
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6, delay: 0.4 }}
              className="text-lg text-gray-600 mb-8"
            >
              Understand your rights. Get Youtube help. Speak freely in your
              language.
            </motion.p>
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6, delay: 0.6 }}
              className="flex flex-wrap gap-4 mb-8"
            >
              <Link
                href="/chat"
                className="bg-blue-900 hover:bg-blue-800 text-white px-6 py-3 rounded-full font-medium transition duration-300 flex items-center"
              >
                <i className="fas fa-comment-dots mr-2"></i> Ask a Legal
                Question
              </Link>
              <a
                href="#demo"
                className="bg-white border border-blue-900 text-blue-900 hover:bg-blue-50 px-6 py-3 rounded-full font-medium transition duration-300 flex items-center"
              >
                <i className="fas fa-play-circle mr-2"></i> Try Demo
              </a>
            </motion.div>
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6, delay: 0.8 }}
              className="flex items-center"
            >
              <div className="bg-green-100 text-green-800 px-4 py-2 rounded-full text-sm font-medium flex items-center">
                <i className="fab fa-whatsapp mr-2"></i>
                Talk on WhatsApp
              </div>
              <div className="ml-4 text-sm text-gray-600">Available 24/7</div>
            </motion.div>
          </motion.div>
          <div className="md:w-1/2 relative">
            <div className="relative">
              <motion.img
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.6 }}
                src="/Images/placeholder.svg"
                alt="Recapify helping a rural person"
                className="w-full max-w-md mx-auto"
              />
              {[
                { name: "Hindi", color: "orange", position: "-top-8 -left-8" },
                {
                  name: "Gujarati",
                  color: "green",
                  position: "-top-4 right-12",
                },
                {
                  name: "Marathi",
                  color: "blue",
                  position: "top-1/4 -right-12",
                },
                {
                  name: "Tamil",
                  color: "purple",
                  position: "top-1/2 -left-12",
                },
                {
                  name: "Telugu",
                  color: "yellow",
                  position: "bottom-1/4 -right-8",
                },
                {
                  name: "Bengali",
                  color: "pink",
                  position: "-bottom-6 left-8",
                },
                {
                  name: "Odia",
                  color: "gray",
                  position: "bottom-1/3 -left-16",
                },
                {
                  name: "Kannada",
                  color: "indigo",
                  position: "top-3/4 -right-16",
                },
              ].map((lang, index) => {
                return (
                  <motion.div
                    key={lang.name}
                    initial={{ opacity: 0, scale: 0.8 }}
                    animate={{ opacity: 1, scale: 1 }}
                    transition={{ duration: 0.6, delay: 0.2 + index * 0.2 }}
                    className={`absolute ${lang.position} bg-${lang.color}-100 text-${lang.color}-600 px-4 py-2 rounded-full text-sm font-semibold`}
                  >
                    {lang.name}
                  </motion.div>
                );
              })}
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
