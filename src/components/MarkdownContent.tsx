import React from "react";

/**
 * Minimal markdown renderer for update descriptions.
 * Supports: ## headings, ### headings, **bold**, - bullet lists, blank-line paragraphs.
 */
export function MarkdownContent({ content }: { content: string }) {
  const lines = content.split("\n");
  const elements: React.ReactNode[] = [];
  let listItems: React.ReactNode[] = [];
  let key = 0;

  const flushList = () => {
    if (listItems.length > 0) {
      elements.push(
        <ul key={key++} className="my-3 space-y-1 pl-5 list-disc text-zinc-300 text-sm leading-relaxed">
          {listItems}
        </ul>
      );
      listItems = [];
    }
  };

  const renderInline = (text: string): React.ReactNode => {
    // Handle **bold** and `code`
    const parts = text.split(/(\*\*[^*]+\*\*|`[^`]+`)/g);
    return parts.map((part, i) => {
      if (part.startsWith("**") && part.endsWith("**")) {
        return <strong key={i} className="text-white font-semibold">{part.slice(2, -2)}</strong>;
      }
      if (part.startsWith("`") && part.endsWith("`")) {
        return <code key={i} className="bg-zinc-800 text-amber-300 px-1.5 py-0.5 rounded text-xs font-mono">{part.slice(1, -1)}</code>;
      }
      return part;
    });
  };

  for (let i = 0; i < lines.length; i++) {
    const line = lines[i];

    if (line.startsWith("## ")) {
      flushList();
      elements.push(
        <h2 key={key++} className="text-base font-semibold text-white mt-6 mb-2 first:mt-0">
          {renderInline(line.slice(3))}
        </h2>
      );
    } else if (line.startsWith("### ")) {
      flushList();
      elements.push(
        <h3 key={key++} className="text-sm font-semibold text-zinc-200 mt-4 mb-1.5">
          {renderInline(line.slice(4))}
        </h3>
      );
    } else if (line.startsWith("- ")) {
      listItems.push(
        <li key={key++}>{renderInline(line.slice(2))}</li>
      );
    } else if (line.trim() === "") {
      flushList();
    } else {
      flushList();
      elements.push(
        <p key={key++} className="text-sm text-zinc-300 leading-relaxed my-2">
          {renderInline(line)}
        </p>
      );
    }
  }

  flushList();
  return <div>{elements}</div>;
}
