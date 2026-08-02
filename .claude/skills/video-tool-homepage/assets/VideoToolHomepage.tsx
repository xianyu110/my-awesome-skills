import type { FormEvent } from "react";
import {
  AudioLines,
  BadgeCheck,
  Captions,
  Check,
  Clipboard,
  Code2,
  Crown,
  Download,
  FileVideo,
  Files,
  Gauge,
  Link as LinkIcon,
  ShieldCheck,
  Sparkles,
  Users,
  type LucideIcon,
} from "lucide-react";

import "./video-tool-homepage.css";

export type VideoToolIcon =
  | "api"
  | "audio"
  | "batch"
  | "captions"
  | "download"
  | "quality"
  | "safety"
  | "teams";

export type VideoToolItem = {
  title: string;
  description: string;
  icon: VideoToolIcon;
  href?: string;
  badge?: string;
  memberOnly?: boolean;
};

export type VideoToolFeature = {
  title: string;
  description: string;
  icon: VideoToolIcon;
};

export type VideoToolUseCase = {
  audience: string;
  title: string;
  description: string;
};

export type VideoToolFaq = {
  question: string;
  answer: string;
};

export type VideoToolExample = {
  eyebrow: string;
  title: string;
  description: string;
  previewImage?: { src: string; alt: string };
  sourceLabel: string;
  sourceValue: string;
  outputLabel: string;
  outputValue: string;
  metadata: string[];
};

export type VideoToolUpgrade = {
  eyebrow: string;
  title: string;
  description: string;
  benefits: string[];
  primaryLabel: string;
  secondaryLabel?: string;
  secondaryHref?: string;
};

export type VideoToolHomepageCopy = {
  navigation: {
    primaryLabel: string;
    tools: string;
    examples: string;
    features: string;
    useCases: string;
    faq: string;
    pricing: string;
  };
  eyebrow: string;
  title: string;
  description: string;
  inputLabel: string;
  inputPlaceholder: string;
  paste: string;
  submit: string;
  submitting: string;
  trustLine: string;
  memberNote: string;
  memberBadge: string;
  toolsEyebrow: string;
  toolsTitle: string;
  toolsDescription: string;
  exampleTitle: string;
  featuresEyebrow: string;
  featuresTitle: string;
  useCasesEyebrow: string;
  useCasesTitle: string;
  faqTitle: string;
  footerDescription: string;
  legalNavigationLabel: string;
};

export type VideoToolHomepageProps = {
  brand: string;
  copy: VideoToolHomepageCopy;
  tools: VideoToolItem[];
  example: VideoToolExample;
  features: VideoToolFeature[];
  useCases: VideoToolUseCase[];
  faqs: VideoToolFaq[];
  upgrade: VideoToolUpgrade;
  value: string;
  onValueChange: (value: string) => void;
  onSubmit: (value: string) => void | Promise<void>;
  onPasteRequested?: () => void | Promise<void>;
  onUpgrade: () => void;
  busy?: boolean;
  logoHref?: string;
  headerAction?: { label: string; href: string };
  legalLinks?: { label: string; href: string }[];
};

const ICONS: Record<VideoToolIcon, LucideIcon> = {
  api: Code2,
  audio: AudioLines,
  batch: Files,
  captions: Captions,
  download: Download,
  quality: Gauge,
  safety: ShieldCheck,
  teams: Users,
};

export function VideoToolHomepage({
  brand,
  copy,
  tools,
  example,
  features,
  useCases,
  faqs,
  upgrade,
  value,
  onValueChange,
  onSubmit,
  onPasteRequested,
  onUpgrade,
  busy = false,
  logoHref = "/",
  headerAction,
  legalLinks = [],
}: VideoToolHomepageProps) {
  function submit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    const normalized = value.trim();
    if (!normalized || busy) return;
    void onSubmit(normalized);
  }

  return (
    <div className="vth-site">
      <header className="vth-header">
        <a className="vth-logo" href={logoHref} aria-label={brand}>
          <span className="vth-logo-mark" aria-hidden="true">
            <FileVideo size={22} />
          </span>
          <span>{brand}</span>
        </a>

        <nav
          className="vth-navigation"
          aria-label={copy.navigation.primaryLabel}
        >
          <a href="#tools">{copy.navigation.tools}</a>
          <a href="#example">{copy.navigation.examples}</a>
          <a href="#features">{copy.navigation.features}</a>
          <a href="#use-cases">{copy.navigation.useCases}</a>
          <a href="#faq">{copy.navigation.faq}</a>
          <a href="#upgrade">{copy.navigation.pricing}</a>
        </nav>

        {headerAction ? (
          <a className="vth-header-action" href={headerAction.href}>
            {headerAction.label}
          </a>
        ) : null}
      </header>

      <main>
        <section className="vth-hero" aria-labelledby="vth-title">
          <div className="vth-hero-copy">
            <p className="vth-eyebrow">
              <Sparkles size={16} aria-hidden="true" />
              {copy.eyebrow}
            </p>
            <h1 id="vth-title">{copy.title}</h1>
            <p>{copy.description}</p>
          </div>

          <form className="vth-tool" onSubmit={submit} aria-busy={busy}>
            <label htmlFor="vth-video-url">{copy.inputLabel}</label>
            <div className="vth-input-row">
              <div className="vth-input-shell">
                <LinkIcon size={19} aria-hidden="true" />
                <input
                  id="vth-video-url"
                  type="url"
                  inputMode="url"
                  autoComplete="url"
                  value={value}
                  placeholder={copy.inputPlaceholder}
                  disabled={busy}
                  onChange={(event) => onValueChange(event.target.value)}
                />
              </div>
              {onPasteRequested ? (
                <button
                  className="vth-paste-button"
                  type="button"
                  disabled={busy}
                  onClick={() => void onPasteRequested()}
                >
                  <Clipboard size={18} aria-hidden="true" />
                  {copy.paste}
                </button>
              ) : null}
            </div>

            <div className="vth-tool-footer">
              <div className="vth-tool-notes">
                <p>
                  <BadgeCheck size={15} aria-hidden="true" />
                  {copy.trustLine}
                </p>
                <a href="#upgrade">
                  <Crown size={15} aria-hidden="true" />
                  {copy.memberNote}
                </a>
              </div>
              <button
                className="vth-primary-button"
                type="submit"
                disabled={busy || !value.trim()}
              >
                <Download size={19} aria-hidden="true" />
                {busy ? copy.submitting : copy.submit}
              </button>
            </div>
          </form>
        </section>

        <section className="vth-section vth-tools" id="tools">
          <div className="vth-section-heading">
            <p>{copy.toolsEyebrow}</p>
            <h2>{copy.toolsTitle}</h2>
            <span>{copy.toolsDescription}</span>
          </div>
          <div className="vth-tool-grid">
            {tools.map((tool) => {
              const Icon = ICONS[tool.icon];
              const contents = (
                <>
                  <span className="vth-tool-icon">
                    <Icon size={24} aria-hidden="true" />
                  </span>
                  <span className="vth-tool-copy">
                    <strong>{tool.title}</strong>
                    <span>{tool.description}</span>
                  </span>
                  {tool.badge || tool.memberOnly ? (
                    <span className="vth-tool-badge">
                      {tool.memberOnly ? (
                        <Crown size={13} aria-hidden="true" />
                      ) : null}
                      {tool.badge || copy.memberBadge}
                    </span>
                  ) : null}
                </>
              );

              return tool.href ? (
                <a className="vth-tool-card" href={tool.href} key={tool.title}>
                  {contents}
                </a>
              ) : (
                <article className="vth-tool-card" key={tool.title}>
                  {contents}
                </article>
              );
            })}
          </div>
        </section>

        <section className="vth-example-band" id="example">
          <div className="vth-example-inner">
            <div className="vth-example-heading">
              <p>{example.eyebrow}</p>
              <h2>{copy.exampleTitle}</h2>
              <span>{example.description}</span>
            </div>
            <article className="vth-result-example">
              {example.previewImage ? (
                <img
                  className="vth-result-preview"
                  src={example.previewImage.src}
                  alt={example.previewImage.alt}
                  width={720}
                  height={405}
                  loading="lazy"
                />
              ) : null}
              <div className="vth-result-status">
                <BadgeCheck size={18} aria-hidden="true" />
                {example.title}
              </div>
              <dl>
                <div>
                  <dt>{example.sourceLabel}</dt>
                  <dd>{example.sourceValue}</dd>
                </div>
                <div>
                  <dt>{example.outputLabel}</dt>
                  <dd>{example.outputValue}</dd>
                </div>
              </dl>
              <div className="vth-result-meta">
                {example.metadata.map((item) => (
                  <span key={item}>{item}</span>
                ))}
              </div>
            </article>
          </div>
        </section>

        <section className="vth-section" id="features">
          <div className="vth-section-heading">
            <p>{copy.featuresEyebrow}</p>
            <h2>{copy.featuresTitle}</h2>
          </div>
          <div className="vth-feature-grid">
            {features.map((feature) => {
              const Icon = ICONS[feature.icon];
              return (
                <article key={feature.title}>
                  <Icon size={25} aria-hidden="true" />
                  <h3>{feature.title}</h3>
                  <p>{feature.description}</p>
                </article>
              );
            })}
          </div>
        </section>

        <section className="vth-use-case-band" id="use-cases">
          <div className="vth-section vth-use-case-inner">
            <div className="vth-section-heading">
              <p>{copy.useCasesEyebrow}</p>
              <h2>{copy.useCasesTitle}</h2>
            </div>
            <div className="vth-use-case-grid">
              {useCases.map((useCase) => (
                <article key={useCase.title}>
                  <span>{useCase.audience}</span>
                  <h3>{useCase.title}</h3>
                  <p>{useCase.description}</p>
                </article>
              ))}
            </div>
          </div>
        </section>

        <section className="vth-section vth-faq" id="faq">
          <div className="vth-section-heading">
            <h2>{copy.faqTitle}</h2>
          </div>
          <div className="vth-faq-list">
            {faqs.map((faq, index) => (
              <details key={faq.question} open={index === 0}>
                <summary>{faq.question}</summary>
                <p>{faq.answer}</p>
              </details>
            ))}
          </div>
        </section>

        <section
          className="vth-upgrade"
          id="upgrade"
          aria-labelledby="vth-upgrade-title"
        >
          <div className="vth-upgrade-inner">
            <div className="vth-upgrade-copy">
              <p>
                <Crown size={17} aria-hidden="true" />
                {upgrade.eyebrow}
              </p>
              <h2 id="vth-upgrade-title">{upgrade.title}</h2>
              <span>{upgrade.description}</span>
            </div>
            <ul>
              {upgrade.benefits.map((benefit) => (
                <li key={benefit}>
                  <Check size={17} aria-hidden="true" />
                  {benefit}
                </li>
              ))}
            </ul>
            <div className="vth-upgrade-actions">
              <button type="button" onClick={onUpgrade}>
                {upgrade.primaryLabel}
              </button>
              {upgrade.secondaryLabel && upgrade.secondaryHref ? (
                <a href={upgrade.secondaryHref}>{upgrade.secondaryLabel}</a>
              ) : null}
            </div>
          </div>
        </section>
      </main>

      <footer className="vth-footer">
        <div>
          <a className="vth-logo" href={logoHref}>
            <span className="vth-logo-mark" aria-hidden="true">
              <FileVideo size={20} />
            </span>
            <span>{brand}</span>
          </a>
          <p>{copy.footerDescription}</p>
        </div>
        {legalLinks.length ? (
          <nav aria-label={copy.legalNavigationLabel}>
            {legalLinks.map((link) => (
              <a href={link.href} key={link.href}>
                {link.label}
              </a>
            ))}
          </nav>
        ) : null}
      </footer>
    </div>
  );
}
