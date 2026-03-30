"""
Multi-Agent Research Pipeline
3 Claude agents working in sequence:
  Agent 1 (Researcher)  — gathers and structures raw information
  Agent 2 (Critic)      — challenges assumptions, finds gaps
  Agent 3 (Writer)      — synthesizes into a polished report
"""
import anthropic
import argparse
import time
from datetime import datetime

client = anthropic.Anthropic()

def call_agent(role: str, system: str, prompt: str, context: str = "") -> str:
    print(f"\n🤖 {role} working...")
    start = time.time()
    
    messages = [{"role": "user", "content": prompt}]
    if context:
        messages = [
            {"role": "user", "content": f"Here is the previous work:\n\n{context}"},
            {"role": "assistant", "content": "I have reviewed the previous work. I'm ready to proceed."},
            {"role": "user", "content": prompt}
        ]
    
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=3000,
        system=system,
        messages=messages
    )
    elapsed = time.time() - start
    print(f"   Done in {elapsed:.1f}s ({response.usage.output_tokens} tokens)")
    return response.content[0].text

def research(topic: str, depth: str = "standard") -> dict:
    print(f"\n{'='*60}")
    print(f"🔬 Research Pipeline: {topic}")
    print(f"{'='*60}")
    
    # Agent 1: Researcher
    researcher_system = """You are a thorough research analyst. Your job is to gather and organize 
comprehensive information on any topic. Be factual, specific, and cite relevant statistics or examples. 
Structure your output with clear sections. Cover: background, key facts, current state, major players/factors, 
data points, and open questions."""

    researcher_prompt = f"""Research the following topic comprehensively:

TOPIC: {topic}

Provide:
1. **Executive Summary** (3-4 sentences)
2. **Background & Context** 
3. **Key Facts & Data Points** (with numbers where possible)
4. **Major Players / Key Factors**
5. **Current Landscape** (what's happening now)
6. **Open Questions** (what remains uncertain or debated)

Be specific. Use real examples. Depth level: {depth}"""

    research_output = call_agent("Researcher", researcher_system, researcher_prompt)
    
    # Agent 2: Critic
    critic_system = """You are a rigorous intellectual critic and devil's advocate. 
Your job is to identify weaknesses, gaps, counterarguments, and overlooked perspectives 
in research. Be constructive but challenging. Your critique makes the final output stronger."""

    critic_prompt = f"""Critically evaluate this research on "{topic}".

Identify:
1. **Gaps** — What important aspects are missing?
2. **Counterarguments** — What would skeptics say?
3. **Assumptions** — What is being taken for granted?
4. **Alternative Perspectives** — What other viewpoints exist?
5. **Verification Needs** — What claims need more evidence?
6. **Improvements** — How should the final report address these issues?

Be specific and constructive."""

    critique_output = call_agent("Critic", critic_system, critic_prompt, research_output)
    
    # Agent 3: Writer
    writer_system = """You are an expert writer who synthesizes research into clear, compelling reports. 
You balance rigor with readability. Your reports are used by decision-makers and are known for being 
accurate, balanced, and actionable."""

    writer_prompt = f"""Write a comprehensive research report on "{topic}".

You have access to:
1. Initial research (comprehensive data gathering)
2. Critical review (identifying gaps and counterarguments)

Synthesize BOTH into a polished final report that:
- Addresses the gaps identified by the critic
- Presents balanced perspectives
- Includes specific data points
- Ends with clear conclusions and implications

Format:
# {topic}: Research Report
*Generated {datetime.now().strftime('%B %d, %Y')}*

## Executive Summary
## Key Findings  
## Detailed Analysis
## Counterarguments & Limitations
## Conclusions & Implications
## Further Reading Suggestions"""

    combined_context = f"RESEARCH:\n{research_output}\n\nCRITIQUE:\n{critique_output}"
    final_report = call_agent("Writer", writer_system, writer_prompt, combined_context)
    
    return {
        "topic": topic,
        "research": research_output,
        "critique": critique_output,
        "final_report": final_report,
        "timestamp": datetime.now().isoformat()
    }

def main():
    parser = argparse.ArgumentParser(description="Multi-Agent Research Pipeline")
    parser.add_argument("topic", help="Topic to research")
    parser.add_argument("--depth", choices=["brief", "standard", "deep"], default="standard")
    parser.add_argument("--save", help="Save outputs to this filename prefix")
    parser.add_argument("--show-all", action="store_true", help="Show all agent outputs")
    args = parser.parse_args()
    
    result = research(args.topic, args.depth)
    
    print("\n" + "="*60)
    print("📄 FINAL REPORT")
    print("="*60)
    print(result["final_report"])
    
    if args.show_all:
        print("\n" + "="*60)
        print("🔬 RAW RESEARCH")
        print("="*60)
        print(result["research"])
        print("\n" + "="*60)
        print("🔍 CRITIQUE")
        print("="*60)
        print(result["critique"])
    
    if args.save:
        import json
        with open(f"{args.save}_full.json", "w") as f:
            json.dump(result, f, indent=2)
        with open(f"{args.save}_report.md", "w") as f:
            f.write(result["final_report"])
        print(f"\n💾 Saved: {args.save}_full.json and {args.save}_report.md")

if __name__ == "__main__":
    main()
