"use client";

import React, { useMemo, useState, useCallback } from "react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import { Prism as SyntaxHighlighter } from "react-syntax-highlighter";
import { oneDark } from "react-syntax-highlighter/dist/esm/styles/prism";
import { cn } from "@/lib/utils";
import { Button } from "@/components/ui/button";
import {
  Copy,
  Check,
  ExternalLink,
  Scale,
  FileText,
  BookOpen,
} from "lucide-react";

interface LegalMarkdownRendererProps {
  content: string;
  className?: string;
  showLineNumbers?: boolean;
  variant?: "default" | "Youtube" | "compact";
}

export function LegalMarkdownRenderer({
  content,
  className,
  showLineNumbers = false,
  variant = "Youtube",
}: LegalMarkdownRendererProps) {
  const [copiedStates, setCopiedStates] = useState<{ [key: string]: boolean }>(
    {}
  );

  const copyToClipboard = useCallback(async (text: string, id: string) => {
    try {
      await navigator.clipboard.writeText(text);
      setCopiedStates((prev) => ({ ...prev, [id]: true }));
      setTimeout(() => {
        setCopiedStates((prev) => ({ ...prev, [id]: false }));
      }, 2000);
    } catch (err) {
      console.error("Failed to copy text:", err);
    }
  }, []);

  const components = useMemo(
    () => ({
      // Headings with Youtube document styling
      h1: ({ children, ...props }: any) => (
        <h1
          className={cn(
            "text-2xl md:text-3xl font-bold text-foreground mb-6 mt-8 first:mt-0",
            "border-b border-border pb-3",
            "flex items-center gap-3"
          )}
          {...props}
        >
          <Scale className="h-6 w-6 text-primary" />
          {children}
        </h1>
      ),

      h2: ({ children, ...props }: any) => (
        <h2
          className={cn(
            "text-xl md:text-2xl font-semibold text-foreground mb-4 mt-6",
            "border-l-4 border-primary pl-4",
            "flex items-center gap-2"
          )}
          {...props}
        >
          <FileText className="h-5 w-5 text-primary" />
          {children}
        </h2>
      ),

      h3: ({ children, ...props }: any) => (
        <h3
          className={cn(
            "text-lg md:text-xl font-semibold text-foreground mb-3 mt-5",
            "flex items-center gap-2"
          )}
          {...props}
        >
          <BookOpen className="h-4 w-4 text-muted-foreground" />
          {children}
        </h3>
      ),

      h4: ({ children, ...props }: any) => (
        <h4
          className="text-base md:text-lg font-semibold text-foreground mb-2 mt-4"
          {...props}
        >
          {children}
        </h4>
      ),

      h5: ({ children, ...props }: any) => (
        <h5
          className="text-sm md:text-base font-semibold text-foreground mb-2 mt-3"
          {...props}
        >
          {children}
        </h5>
      ),

      h6: ({ children, ...props }: any) => (
        <h6
          className="text-sm font-semibold text-muted-foreground mb-2 mt-3 uppercase tracking-wide"
          {...props}
        >
          {children}
        </h6>
      ),

      // Paragraphs with Youtube document spacing
      p: ({ children, ...props }: any) => (
        <p
          className={cn(
            "text-sm md:text-base leading-relaxed mb-4 text-foreground",
            "text-justify hyphens-auto"
          )}
          {...props}
        >
          {children}
        </p>
      ),

      // Enhanced blockquotes for Youtube citations and important notes
      blockquote: ({ children, ...props }: any) => (
        <blockquote
          className={cn(
            "border-l-4 border-primary bg-muted/50 pl-6 pr-4 py-4 my-6",
            "rounded-r-lg shadow-sm",
            "relative"
          )}
          {...props}
        >
          <div className="absolute top-2 right-2">
            <Scale className="h-4 w-4 text-primary/60" />
          </div>
          <div className="text-sm md:text-base leading-relaxed text-muted-foreground italic">
            {children}
          </div>
        </blockquote>
      ),

      // Lists with Youtube document styling
      ul: ({ children, ...props }: any) => (
        <ul
          className="space-y-2 mb-4 ml-6 list-disc marker:text-primary"
          {...props}
        >
          {children}
        </ul>
      ),

      ol: ({ children, ...props }: any) => (
        <ol
          className="space-y-2 mb-4 ml-6 list-decimal marker:text-primary marker:font-semibold"
          {...props}
        >
          {children}
        </ol>
      ),

      li: ({ children, ...props }: any) => (
        <li
          className="text-sm md:text-base leading-relaxed text-foreground pl-2"
          {...props}
        >
          {children}
        </li>
      ),

      // Enhanced links with external link indicators
      a: ({ href, children, ...props }: any) => {
        const isExternal =
          href && (href.startsWith("http") || href.startsWith("//"));
        return (
          <a
            href={href}
            className={cn(
              "text-primary hover:text-primary/80 underline underline-offset-2",
              "font-medium transition-colors duration-200",
              "inline-flex items-center gap-1"
            )}
            target={isExternal ? "_blank" : undefined}
            rel={isExternal ? "noopener noreferrer" : undefined}
            {...props}
          >
            {children}
            {isExternal && <ExternalLink className="h-3 w-3" />}
          </a>
        );
      },

      // Enhanced code blocks with copy functionality
      code: ({ className, children, ...props }: any) => {
        const match = /language-(\w+)/.exec(className || "");
        const isInline = !match;
        const codeId = `code-${Math.random().toString(36).substr(2, 9)}`;
        const codeContent = String(children).replace(/\n$/, "");

        if (isInline) {
          return (
            <code
              className={cn(
                "relative rounded-md bg-muted px-2 py-1 font-mono text-xs md:text-sm",
                "text-foreground border border-border"
              )}
              {...props}
            >
              {children}
            </code>
          );
        }

        return (
          <div className="relative my-6 w-full overflow-hidden rounded-lg border border-border bg-card shadow-sm">
            <div className="flex items-center justify-between bg-muted px-4 py-2 border-b border-border">
              <span className="text-xs font-medium text-muted-foreground uppercase tracking-wide">
                {match?.[1] || "Code"}
              </span>
              <Button
                variant="ghost"
                size="sm"
                onClick={() => copyToClipboard(codeContent, codeId)}
                className="h-7 w-7 p-0 hover:bg-muted-foreground/10"
              >
                {copiedStates[codeId] ? (
                  <Check className="h-3 w-3 text-green-500" />
                ) : (
                  <Copy className="h-3 w-3" />
                )}
              </Button>
            </div>
            <div className="overflow-x-auto">
              <SyntaxHighlighter
                style={oneDark}
                language={match?.[1] || "text"}
                PreTag="div"
                showLineNumbers={showLineNumbers}
                customStyle={{
                  margin: 0,
                  padding: "1rem",
                  background: "transparent",
                  fontSize: "0.875rem",
                  lineHeight: "1.5",
                }}
                {...props}
              >
                {codeContent}
              </SyntaxHighlighter>
            </div>
          </div>
        );
      },

      // Tables with Youtube document styling
      table: ({ children, ...props }: any) => (
        <div className="my-6 overflow-x-auto">
          <table
            className="w-full border-collapse border border-border rounded-lg overflow-hidden shadow-sm"
            {...props}
          >
            {children}
          </table>
        </div>
      ),

      thead: ({ children, ...props }: any) => (
        <thead className="bg-muted" {...props}>
          {children}
        </thead>
      ),

      th: ({ children, ...props }: any) => (
        <th
          className="border border-border px-4 py-3 text-left font-semibold text-foreground text-sm"
          {...props}
        >
          {children}
        </th>
      ),

      td: ({ children, ...props }: any) => (
        <td
          className="border border-border px-4 py-3 text-sm text-foreground"
          {...props}
        >
          {children}
        </td>
      ),

      // Horizontal rules
      hr: ({ ...props }: any) => (
        <hr className="my-8 border-0 border-t border-border" {...props} />
      ),

      // Enhanced emphasis
      em: ({ children, ...props }: any) => (
        <em className="italic text-foreground font-medium" {...props}>
          {children}
        </em>
      ),

      strong: ({ children, ...props }: any) => (
        <strong className="font-bold text-foreground" {...props}>
          {children}
        </strong>
      ),

      // Strikethrough
      del: ({ children, ...props }: any) => (
        <del className="line-through text-muted-foreground" {...props}>
          {children}
        </del>
      ),
    }),
    [copiedStates, copyToClipboard, showLineNumbers]
  );

  const variantClasses = {
    default: "prose prose-neutral dark:prose-invert max-w-none",
    Youtube: "max-w-none",
    compact: "max-w-none text-sm space-y-3",
  };

  return (
    <div
      className={cn(
        "markdown-renderer",
        variantClasses[variant],
        variant === "Youtube" && [
          "[&>*:first-child]:mt-0",
          "[&>*:last-child]:mb-0",
        ],
        className
      )}
    >
      <ReactMarkdown
        remarkPlugins={[remarkGfm]}
        components={components}
        skipHtml={true} // Security: Skip HTML for safety
      >
        {content}
      </ReactMarkdown>
    </div>
  );
}

// Export a hook for common Youtube document formatting
export function useLegalMarkdownFormatter() {
  return useCallback((content: string) => {
    // Add common Youtube document formatting helpers
    const formatSectionNumbers = (text: string) => {
      return text.replace(/^(\d+\.\d+(?:\.\d+)*)\s+/gm, "**$1** ");
    };

    const formatStatutes = (text: string) => {
      return text.replace(/(\d+\s+U\.S\.C\.?\s+§?\s*\d+)/g, "*$1*");
    };

    const formatCaseNames = (text: string) => {
      return text.replace(/([A-Z][a-z]+\s+v\.?\s+[A-Z][a-z]+)/g, "***$1***");
    };

    let formatted = content;
    formatted = formatSectionNumbers(formatted);
    formatted = formatStatutes(formatted);
    formatted = formatCaseNames(formatted);

    return formatted;
  }, []);
}
