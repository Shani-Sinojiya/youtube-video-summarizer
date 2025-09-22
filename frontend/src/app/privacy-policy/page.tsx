"use client";
import React from "react";
import Link from "next/link";
import { motion } from "framer-motion";
import Logo from "@/components/logo";

const PrivacyPolicyPage = () => {
  const itemVariants = {
    hidden: { opacity: 0, y: 20 },
    visible: {
      opacity: 1,
      y: 0,
      transition: { duration: 0.6, ease: "easeOut" },
    },
  };

  const headerVariants = {
    hidden: { opacity: 0, y: -50 },
    visible: {
      opacity: 1,
      y: 0,
      transition: { duration: 0.6, ease: "easeOut" },
    },
  };

  const sectionVariants = {
    hidden: { opacity: 0, x: -30 },
    visible: {
      opacity: 1,
      x: 0,
      transition: { duration: 0.8, ease: "easeOut" },
    },
  };

  const footerVariants = {
    hidden: { opacity: 0, y: 50 },
    visible: {
      opacity: 1,
      y: 0,
      transition: { duration: 0.6, ease: "easeOut", delay: 0.3 },
    },
  };

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

  return (
    <div className="min-h-screen bg-white">
      {/* Header */}
      <motion.header
        variants={headerVariants}
        initial="hidden"
        animate="visible"
        className="bg-white shadow-sm border-b"
      >
        <div className="max-w-4xl mx-auto px-4 py-4">
          <motion.div
            whileHover={{ scale: 1.05 }}
            transition={{ duration: 0.2 }}
          >
            <Link
              href="/"
              className="flex items-center text-blue-900 hover:text-blue-700"
            >
              <div className="w-8 h-8 rounded-full bg-blue-900 flex items-center justify-center text-white font-bold text-sm mr-2">
                <Logo className="w-6 h-6" />
              </div>
              <span className="text-lg font-semibold">Recapify</span>
            </Link>
          </motion.div>
        </div>
      </motion.header>

      {/* Content */}
      <motion.div
        variants={containerVariants}
        initial="hidden"
        animate="visible"
        className="max-w-4xl mx-auto px-4 py-12"
      >
        <div className="prose prose-blue max-w-none">
          <motion.h1
            variants={itemVariants}
            className="text-4xl font-bold text-blue-900 mb-8"
          >
            Privacy Policy
          </motion.h1>

          <motion.p variants={itemVariants} className="text-gray-600 mb-8">
            <strong>Last updated:</strong>{" "}
            {new Date().toLocaleDateString("en-US", {
              year: "numeric",
              month: "long",
              day: "numeric",
            })}
          </motion.p>

          <div className="space-y-8">
            {[
              {
                title: "1. Introduction",
                content: (
                  <motion.p
                    variants={itemVariants}
                    className="text-gray-700 leading-relaxed"
                  >
                    Recapify ("we," "our," or "us") is committed to protecting
                    your privacy. This Privacy Policy explains how we collect,
                    use, disclose, and safeguard your information when you use
                    our AI-powered Youtube assistance platform, including our
                    website, mobile application, and voice services.
                  </motion.p>
                ),
              },
              {
                title: "2. Information We Collect",
                content: (
                  <motion.div variants={itemVariants} className="space-y-4">
                    <div>
                      <h3 className="text-lg font-medium text-gray-900 mb-2">
                        2.1 Information You Provide
                      </h3>
                      <ul className="list-disc list-inside text-gray-700 space-y-1">
                        <li>
                          Legal questions and queries submitted to our AI system
                        </li>
                        <li>
                          Voice recordings when using voice-to-voice features
                        </li>
                        <li>Account information (if you create an account)</li>
                        <li>Contact information for Youtube aid referrals</li>
                        <li>
                          Feedback and correspondence with our support team
                        </li>
                      </ul>
                    </div>

                    <div>
                      <h3 className="text-lg font-medium text-gray-900 mb-2">
                        2.2 Automatically Collected Information
                      </h3>
                      <ul className="list-disc list-inside text-gray-700 space-y-1">
                        <li>
                          Device information (type, operating system, browser)
                        </li>
                        <li>Usage analytics and interaction patterns</li>
                        <li>IP address and approximate location</li>
                        <li>Session data and conversation logs</li>
                      </ul>
                    </div>
                  </motion.div>
                ),
              },
              {
                title: "3. How We Use Your Information",
                content: (
                  <motion.ul
                    variants={itemVariants}
                    className="list-disc list-inside text-gray-700 space-y-2"
                  >
                    <li>Provide AI-powered Youtube information and guidance</li>
                    <li>
                      Improve our natural language processing capabilities
                    </li>
                    <li>Analyze usage patterns to enhance user experience</li>
                    <li>
                      Connect you with appropriate Youtube aid services when
                      requested
                    </li>
                    <li>
                      Ensure compliance with Youtube and regulatory requirements
                    </li>
                    <li>Detect and prevent fraud or misuse of our services</li>
                  </motion.ul>
                ),
              },
              {
                title: "4. Data Security and Protection",
                content: (
                  <motion.div variants={itemVariants} className="space-y-4">
                    <p className="text-gray-700">
                      We implement industry-standard security measures to
                      protect your information:
                    </p>
                    <ul className="list-disc list-inside text-gray-700 space-y-1">
                      <li>End-to-end encryption for all communications</li>
                      <li>Secure data storage with regular backups</li>
                      <li>Limited access controls for our staff</li>
                      <li>Regular security audits and updates</li>
                      <li>Compliance with Indian data protection laws</li>
                    </ul>
                  </motion.div>
                ),
              },
              {
                title: "5. Data Sharing and Disclosure",
                content: (
                  <motion.div variants={itemVariants}>
                    <p className="text-gray-700 mb-4">
                      We do not sell, trade, or rent your personal information.
                      We may share your information only in the following
                      circumstances:
                    </p>
                    <ul className="list-disc list-inside text-gray-700 space-y-1">
                      <li>
                        With Youtube aid organizations when you request
                        assistance
                      </li>
                      <li>
                        To comply with Youtube obligations or court orders
                      </li>
                      <li>To protect our rights, property, or safety</li>
                      <li>
                        With service providers who assist in operating our
                        platform (under strict confidentiality agreements)
                      </li>
                    </ul>
                  </motion.div>
                ),
              },
              {
                title: "6. Your Rights and Choices",
                content: (
                  <motion.div variants={itemVariants}>
                    <p className="text-gray-700 mb-4">
                      You have the following rights regarding your personal
                      information:
                    </p>
                    <ul className="list-disc list-inside text-gray-700 space-y-1">
                      <li>
                        Access and review the information we have about you
                      </li>
                      <li>Request correction of inaccurate information</li>
                      <li>Request deletion of your personal data</li>
                      <li>Opt-out of certain data processing activities</li>
                      <li>
                        Data portability (receiving your data in a structured
                        format)
                      </li>
                    </ul>
                  </motion.div>
                ),
              },
              {
                title: "7. Children's Privacy",
                content: (
                  <motion.p variants={itemVariants} className="text-gray-700">
                    Recapify is not intended for children under 13 years of age.
                    We do not knowingly collect personal information from
                    children under 13. If you believe we have collected
                    information from a child under 13, please contact us
                    immediately.
                  </motion.p>
                ),
              },
              {
                title: "8. International Data Transfers",
                content: (
                  <motion.p variants={itemVariants} className="text-gray-700">
                    Your information is primarily stored and processed in India.
                    If we transfer data internationally, we ensure appropriate
                    safeguards are in place to protect your information in
                    accordance with applicable data protection laws.
                  </motion.p>
                ),
              },
              {
                title: "9. Changes to This Privacy Policy",
                content: (
                  <motion.p variants={itemVariants} className="text-gray-700">
                    We may update this Privacy Policy from time to time. We will
                    notify you of any material changes by posting the new
                    Privacy Policy on this page and updating the "Last updated"
                    date. Your continued use of Recapify after any changes
                    constitutes acceptance of the updated policy.
                  </motion.p>
                ),
              },
              {
                title: "10. Contact Us",
                content: (
                  <motion.div variants={itemVariants}>
                    <p className="text-gray-700 mb-4">
                      If you have any questions about this Privacy Policy or our
                      data practices, please contact us:
                    </p>
                    <motion.div
                      className="bg-gray-50 p-4 rounded-lg"
                      whileHover={{ scale: 1.02 }}
                      transition={{ duration: 0.2 }}
                    >
                      <p className="text-gray-700">
                        <strong>Email:</strong> privacy@nyayamitra.org
                        <br />
                        <strong>Phone:</strong> 1800-123-4567
                        <br />
                        <strong>Address:</strong> Recapify Legal Tech Pvt. Ltd.
                        <br />
                        Legal Technology Center, Mumbai, Maharashtra, India
                      </p>
                    </motion.div>
                  </motion.div>
                ),
              },
            ].map((section, index) => (
              <motion.section
                key={index}
                variants={sectionVariants}
                initial="hidden"
                whileInView="visible"
                viewport={{ once: true, margin: "-100px" }}
              >
                <motion.h2
                  variants={itemVariants}
                  className="text-2xl font-semibold text-blue-900 mb-4"
                >
                  {section.title}
                </motion.h2>
                {section.content}
              </motion.section>
            ))}
          </div>
        </div>
      </motion.div>

      {/* Footer */}
      <motion.footer
        variants={footerVariants}
        initial="hidden"
        whileInView="visible"
        viewport={{ once: true }}
        className="bg-gray-50 border-t mt-16"
      >
        <div className="max-w-4xl mx-auto px-4 py-8">
          <div className="flex flex-col md:flex-row justify-between items-center">
            <motion.div whileHover={{ x: -5 }} transition={{ duration: 0.2 }}>
              <Link
                href="/"
                className="text-blue-900 hover:text-blue-700 mb-4 md:mb-0"
              >
                ← Back to Recapify
              </Link>
            </motion.div>
            <motion.div
              className="flex space-x-6 text-sm text-gray-600"
              variants={containerVariants}
            >
              {[
                {
                  href: "/privacy-policy",
                  text: "Privacy Policy",
                  active: true,
                },
                { href: "/terms-of-service", text: "Terms of Service" },
                { href: "/disclaimer", text: "Disclaimer" },
              ].map((link, index) => (
                <motion.div
                  key={index}
                  variants={itemVariants}
                  whileHover={{ y: -2 }}
                  transition={{ duration: 0.2 }}
                >
                  <Link
                    href={link.href}
                    className={
                      link.active
                        ? "font-medium text-blue-900"
                        : "hover:text-blue-900"
                    }
                  >
                    {link.text}
                  </Link>
                </motion.div>
              ))}
            </motion.div>
          </div>
        </div>
      </motion.footer>
    </div>
  );
};

export default PrivacyPolicyPage;
