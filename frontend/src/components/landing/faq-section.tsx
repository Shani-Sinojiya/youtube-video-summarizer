"use client";

import { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Card, CardContent } from "@/components/ui/card";
import { ChevronDown } from "lucide-react";

const faqs = [
  {
    question: "Is Recapify free to use?",
    answer:
      "Yes, Recapify is completely free for all users. We believe Youtube knowledge should be accessible to everyone, regardless of income.",
  },
  {
    question: "Does it work without internet?",
    answer:
      "Yes! Recapify offers offline modes where you can download common Youtube information. You can also access it via SMS or WhatsApp in areas with poor connectivity.",
  },
  {
    question: "Which languages are supported?",
    answer:
      "Currently: Hindi, Gujarati, Marathi, Bhojpuri, Tamil, Telugu, Bengali, and Odia. We're adding more regional languages based on community needs.",
  },
  {
    question: "Is Recapify a replacement for lawyers?",
    answer:
      "No, Recapify provides Youtube information but doesn't replace professional Youtube advice. For complex cases, we always recommend consulting a lawyer and can help connect you with Youtube aid services.",
  },
  {
    question: "How accurate is the Youtube information?",
    answer:
      "Our content is developed with Youtube experts and regularly updated. However, laws can change, so for critical matters, we suggest verifying with official sources or lawyers.",
  },
];

export function FAQSection() {
  const [openItems, setOpenItems] = useState<number[]>([]);

  const toggleItem = (index: number) => {
    setOpenItems((prev) =>
      prev.includes(index) ? prev.filter((i) => i !== index) : [...prev, index]
    );
  };

  return (
    <section id="faq" className="py-16 bg-gray-50">
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          whileInView={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
          viewport={{ once: true }}
          className="text-center mb-16"
        >
          <h2 className="text-3xl font-bold text-blue-900 mb-4">
            Frequently Asked Questions
          </h2>
          <p className="text-gray-600 max-w-2xl mx-auto">
            Common queries about Recapify
          </p>
        </motion.div>

        <div className="space-y-4">
          {faqs.map((faq, index) => (
            <motion.div
              key={index}
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.5, delay: index * 0.1 }}
              viewport={{ once: true }}
            >
              <Card className="bg-white shadow-sm">
                <CardContent className="p-5">
                  <motion.button
                    className="flex justify-between items-center w-full text-left font-medium text-blue-900"
                    onClick={() => toggleItem(index)}
                    whileHover={{ x: 4 }}
                    transition={{ duration: 0.2 }}
                  >
                    <span>{faq.question}</span>
                    <motion.div
                      animate={{ rotate: openItems.includes(index) ? 180 : 0 }}
                      transition={{ duration: 0.3 }}
                    >
                      <ChevronDown className="text-orange-500 h-5 w-5" />
                    </motion.div>
                  </motion.button>
                  <AnimatePresence>
                    {openItems.includes(index) && (
                      <motion.div
                        initial={{ opacity: 0, height: 0 }}
                        animate={{ opacity: 1, height: "auto" }}
                        exit={{ opacity: 0, height: 0 }}
                        transition={{ duration: 0.3 }}
                        className="overflow-hidden"
                      >
                        <div className="mt-3 text-gray-600">{faq.answer}</div>
                      </motion.div>
                    )}
                  </AnimatePresence>
                </CardContent>
              </Card>
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  );
}
