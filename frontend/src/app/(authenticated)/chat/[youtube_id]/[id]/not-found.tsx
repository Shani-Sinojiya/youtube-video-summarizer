import Link from "next/link";
import React from "react";

const NotFound = () => {
  return (
    <div className="flex flex-col items-center justify-center min-h-full space-y-4 text-center">
      <h1 className="text-4xl font-bold tracking-tighter sm:text-5xl">
        Chat Not Found
      </h1>
      <p className="max-w-[600px] text-gray-500 md:text-xl/relaxed lg:text-base/relaxed xl:text-xl/relaxed dark:text-gray-400">
        The chat session you are looking for does not exist or has been deleted.
      </p>
      <div className="flex gap-2">
        <Link
          href="/chat"
          className="inline-flex h-10 items-center justify-center rounded-md bg-gray-900 px-8 text-sm font-medium text-gray-50 shadow transition-colors hover:bg-gray-900/90 focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-gray-950 disabled:pointer-events-none disabled:opacity-50 dark:bg-gray-50 dark:text-gray-900 dark:hover:bg-gray-50/90 dark:focus-visible:ring-gray-300"
        >
          Return to New Chat
        </Link>
      </div>
    </div>
  );
};

export default NotFound;
