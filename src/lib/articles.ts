// IMPORTANT: Add new articles here. Keep sorted newest first.
// Tags should be reused consistently for filtering.
//
// Writing rules:
// - Never use em dashes or long dashes. Use commas, periods, or rewrite instead.
// - Links use the "link" section type with href and text fields.

export interface ArticleSection {
  type: "h2" | "h3" | "h4" | "p" | "image" | "video" | "ul" | "ol" | "link";
  text?: string;
  src?: string;
  alt?: string;
  caption?: string;
  items?: string[];
  href?: string;
}

export interface Article {
  id: string;
  title: string;
  description: string;
  publishedAt: string;
  updatedAt?: string;
  heroImage: string;
  tags: string[];
  tldr: string;
  content: ArticleSection[];
}

export const articles: Article[] = [
  {
    id: "how-to-get-free-sports-cards",
    title: "How to Get Free Sports Cards and Where to Get Them",
    publishedAt: "2026-03-28",
    description:
      "Collectors can score free sports cards, packs, and even boxes through live breaks on platforms like Fanatics Live, Whatnot, and TikTok Live. Here's how.",
    heroImage: "/articles/how-to-get-free-sports-cards.jpeg",
    tags: ["free cards", "breaks", "whatnot", "fanatics live", "tiktok live", "beginner"],
    tldr: "You can get free sports cards by participating in live breaks on platforms like Whatnot, Fanatics Live, and TikTok Live. Breakers regularly give away packs and cards to viewers through giveaways, often called \"givvys.\" Following the right accounts and showing up to live streams is the easiest way to start collecting for free. All you have to do is show up, engage, and click enter when a giveaway goes live.",
    content: [
      {
        type: "h2",
        text: "What Are Free Sports Cards?",
      },
      {
        type: "p",
        text: "Free sports cards are cards given away at no cost by breakers, platforms, or brands. This can include individual singles, full packs, or even entire boxes in some cases. Whether it's a breaker tossing a bonus card into a shipment or a platform running a first-time buyer promotion, there are more opportunities to get free cards than most collectors realize.",
      },
      {
        type: "h2",
        text: "How to Get Free Sports Cards",
      },
      {
        type: "p",
        text: "The three main ways to get free sports cards are through live breaks, giveaways during livestreams, and platform-level promotions. Each method is accessible to anyone. You don't need to spend money or have a large collection to take advantage of them.",
      },
      {
        type: "h3",
        text: "1. Participate in Live Breaks",
      },
      {
        type: "p",
        text: "A live break is a livestreamed event where a host opens packs or boxes of cards on camera and distributes the cards to buyers or giveaway winners. Many breakers give away cards to active viewers, new followers, or subscribers as part of their streams. Simply watching and engaging in chat can be enough to score free cards during a break.",
      },
      {
        type: "h3",
        text: "2. Enter Giveaways on Livestreams",
      },
      {
        type: "p",
        text: "Most live break hosts run regular giveaways during their streams. These can include free packs, random cards, or even spots in a paid break at no cost. Viewers typically need to follow the account, comment, or share to enter. Giveaways are one of the most common ways breakers build their audience, so they happen frequently across all major platforms.",
      },
      {
        type: "h3",
        text: "3. Take Advantage of Platform Promotions",
      },
      {
        type: "p",
        text: "Platforms like Whatnot, Fanatics Live, and TikTok Live frequently run their own promotions that include free credits, shipping discounts, or free break spots for new users or during special events. These promotions are often time-limited and tied to new product releases or platform milestones, so it pays to keep an eye out.",
      },
      {
        type: "h2",
        text: "What is a Givvy?",
      },
      {
        type: "p",
        text: "On Whatnot, Fanatics Live, and TikTok Live, giveaways are commonly referred to as \"givvys.\" Live breaks often include givvys to help engage with the live audience. On Whatnot, winning a givvy will usually grant the recipient free delivery or reduced delivery fees on additional purchases within that live break. Breakers run givvys for a few reasons: they help work with the platform algorithm to attract more viewers, they give viewers free or reduced shipping which can encourage them to buy into a break spot, and they are a great way to give back to those who are watching the stream.",
      },
      {
        type: "h2",
        text: "What Are Examples of Giveaways?",
      },
      {
        type: "p",
        text: "Giveaways can range in value from random cards, single cards, graded slabs, packs, blaster boxes, retail boxes, or even entry into a hobby box break at the end of the stream. Sometimes a giveaway will result in an opportunity to get into a break by way of a duck race. Overall, givvys are the easiest way for collectors to get free sports cards. Essentially, viewers are exchanging their time and attention in a live stream to be considered for a giveaway.",
      },
      {
        type: "h2",
        text: "How to Enter a Giveaway",
      },
      {
        type: "p",
        text: "Live viewers have to click an \"Enter\" button while they are in a live stream to enter a giveaway. The breaker running the stream will determine when the giveaway runs. A random wheel spin rolls on screen and the username shown is the winner. It is that simple.",
      },
      {
        type: "link",
        text: "Learn more about how Whatnot giveaways work",
        href: "https://help.whatnot.com/hc/en-us/articles/11329417780365-Giveaways-Overview",
      },
      {
        type: "link",
        text: "Tips for winning Whatnot giveaways",
        href: "https://www.royalvotes.com/how-to-win-whatnot-giveaways.html",
      },
      {
        type: "h2",
        text: "How Many Giveaways Can Someone Win?",
      },
      {
        type: "p",
        text: "Live viewers can enter and win as many giveaways as they wish during a stream. There is no cap or limitation on how many givvys someone can win. However, if someone wins multiple giveaways during the same stream, it is considered respectful to stop entering future givvys so that other viewers have a fair chance to win.",
      },
      {
        type: "h2",
        text: "How Do I Know What the Giveaway Is?",
      },
      {
        type: "p",
        text: "The givvy is usually displayed on screen so you know what you are entering to win. Breakers will often place a small sticky note on the item or below the giveaway that says \"Givvy\" so live viewers can clearly see what they could potentially win.",
      },
      {
        type: "h2",
        text: "What Do I Do If I Win a Giveaway?",
      },
      {
        type: "p",
        text: "Thank the breaker for offering up the giveaway. It is also a nice gesture to consider participating in the break if you win, though this always depends on your financial situation and whether you can afford a spot. There is no obligation to buy in.",
      },
      {
        type: "h2",
        text: "What is the Difference Between a Giveaway and a Buyers Giveaway?",
      },
      {
        type: "p",
        text: "A buyers giveaway, or buyers givvy, is reserved for live viewers who have already purchased a spot in the break. Those viewers can then participate in the buyers givvy when the streamer puts it up. There is a workaround that is generally frowned upon in the hobby community. Live viewers can fill out the entry form during a buyers givvy before the winner is chosen, even without purchasing a spot. Most streamers are unhappy about this because the buyers giveaway is designed to reward those who bought into the break, not those who did not.",
      },
      {
        type: "h2",
        text: "Where Can I Enter Giveaways?",
      },
      {
        type: "p",
        text: "Whatnot, TikTok Live, and Fanatics Live all offer the giveaway feature for live streamers. Streamers can set up givvys before the stream and then initiate them while live. A few things to keep in mind: if you enter a giveaway and then scroll away or leave the stream, your entry will be removed from consideration. The giveaway process is designed to reward those who are actively present in the stream. Some streamers will also require you to be watching to receive your prize.",
      },
      {
        type: "link",
        text: "Learn more about giveaways on TikTok Live",
        href: "https://seller-sg.tiktok.com/university/essay?knowledge_id=7439492894476034&default_language=en&identity=1",
      },
      {
        type: "h2",
        text: "Where to Get Free Sports Cards",
      },
      {
        type: "h3",
        text: "Whatnot",
      },
      {
        type: "p",
        text: "Whatnot is one of the most popular live shopping platforms for sports cards. Breakers on Whatnot regularly host giveaways for their viewers and new followers. Whatnot itself occasionally offers new user promotions that include free credits you can use toward a break. To get started, create an account, follow top sports card breakers, and tune in to their live streams. Many hosts give away cards within the first few minutes of going live.",
      },
      {
        type: "h3",
        text: "Fanatics Live",
      },
      {
        type: "p",
        text: "Fanatics Live is the live commerce platform from Fanatics, one of the biggest names in sports merchandise. The platform has been growing rapidly and regularly features breakers doing live pack openings and giveaways. Fanatics Live also runs platform-wide promotions, especially around major sports events and new card set releases. Creating an account and watching a few streams is all it takes to start participating.",
      },
      {
        type: "h3",
        text: "TikTok Live",
      },
      {
        type: "p",
        text: "TikTok has become a major destination for sports card breakers. Many TikTok creators host live breaks where they open packs on camera and give cards to viewers through comments, games, or random drawings. Following sports card accounts on TikTok and turning on notifications for their live streams gives you the best chance of catching giveaways as they happen. TikTok Live is especially good for beginners since streams are easy to discover through the For You page.",
      },
      {
        type: "h2",
        text: "Tips for Maximizing Your Chances of Getting Free Cards",
      },
      {
        type: "ul",
        items: [
          "Follow your favorite breakers on all platforms so you never miss a live stream",
          "Turn on notifications so you're alerted when a breaker goes live",
          "Engage in chat. Many breakers reward active, positive viewers with free cards",
          "Check in at the start of streams when most giveaways are announced",
          "Join breaker communities on Discord where giveaways are often posted",
          "Look for new user promotions on Whatnot and Fanatics Live when signing up",
        ],
      },
      {
        type: "h2",
        text: "Why Did My Account Get Flagged for Unusual Giveaway Activity?",
      },
      {
        type: "p",
        text: "If you enter too many giveaways in a short duration of time, your account can get flagged for unusual giveaway activity. On Whatnot, your account will be restricted from entering giveaways for a couple days to a couple weeks. After that period of time, your account will be removed from the giveaway timeout and you will be able to enter giveaways again.",
      },
      {
        type: "h2",
        text: "Final Thoughts",
      },
      {
        type: "p",
        text: "Getting free sports cards is very possible with the right approach. The live break community is active, generous, and constantly growing. Whether you're a new collector or just looking to expand your collection without spending, tuning into live breaks on Whatnot, Fanatics Live, and TikTok Live is your best starting point. Show up, engage, and the cards will follow.",
      },
    ],
  },
];

export function getArticleById(id: string): Article | undefined {
  return articles.find((a) => a.id === id);
}

export function getAdjacentArticles(id: string): { prev: Article | null; next: Article | null } {
  const idx = articles.findIndex((a) => a.id === id);
  return {
    prev: idx > 0 ? articles[idx - 1] : null,
    next: idx < articles.length - 1 ? articles[idx + 1] : null,
  };
}

export function getAllTags(): string[] {
  const tagSet = new Set<string>();
  for (const a of articles) {
    for (const t of a.tags) tagSet.add(t);
  }
  return Array.from(tagSet).sort();
}
