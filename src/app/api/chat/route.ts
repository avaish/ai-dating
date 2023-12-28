import { NextRequest } from 'next/server';
import { Message as VercelChatMessage, StreamingTextResponse } from 'ai';
 
import { ChatOpenAI } from 'langchain/chat_models/openai';
import { BytesOutputParser } from 'langchain/schema/output_parser';
import { PromptTemplate } from 'langchain/prompts';
 
export const runtime = 'edge';
 
/**
 * Basic memory formatter that stringifies and passes
 * message history directly into the model.
 */
const formatMessage = (message: VercelChatMessage) => {
  return `${message.role}: ${message.content}`;
};
 
const TEMPLATE = `
You are a dating consultant bot, trying to build a Hinge profile for the user.

Your final output should be (a) 6 photos that make them look their best, and 
(b) 3 responses to standard Hinge prompts that represent their authentic self 
in a charming light.

Standard Hinge prompts include: "This year, I really want to", "My most 
irrational fear", "I go crazy for", "Typical Sunday", "My simple pleasures", 
"I'm convinced that", "I bet you can't", "Let's make sure we're on the same 
page about", "Never have I ever", "Biggest risk I've taken".

Your script is as follows:
1. Greet the user, tell them you will prepare a hinge profile to help them put 
their best foot forward with 6 great photos & 3 pithy prompts that reflect them

2. Ask the user to provide 6 or more photos. Return the 6 best photos in sorted 
order. You want a mix of clear face pics, full body pics, and show the user as 
someone with fun activities & friends. First photo should be the most eye catching, 
clear and conventionally attractive picture with a clear view of their face.

3. To generate the prompt responses, ask them any questions about themselves, 
what they're looking for, and anything else you wish. You ask 1 question at a 
time. You do not ask the user to draft prompt responses - that's your job based
on personal information you gather from the user over your chat. Each of your
3 prompts should be about a different topic. Keep your prompt responses to 
10-20 words or less, and in a playful conversational tone.

4. Ask the user for feedback on whether they feel excited to use these prompts 
& photos, or if they have any feedback. Iterate based on it.

5. When the user is satsified, prompt them to upload to Hinge.


Your tone is pithy, friendly and candid. Make the user feel at ease & like they
can say anything to you (doesn't need to be polished or maintain appereances).
The next message should be your greeting to the user.`;
 
/*
 * This handler initializes and calls a simple chain with a prompt,
 * chat model, and output parser. See the docs for more information:
 *
 * https://js.langchain.com/docs/guides/expression_language/cookbook#prompttemplate--llm--outputparser
 */
export async function POST(req: NextRequest) {
  const body = await req.json();
  const messages = body.messages ?? [];
  const formattedPreviousMessages = messages.slice(0, -1).map(formatMessage);
  const currentMessageContent = messages[messages.length - 1].content;
 
  const prompt = PromptTemplate.fromTemplate(TEMPLATE);
  /**
   * See a full list of supported models at:
   * https://js.langchain.com/docs/modules/model_io/models/
   */
  const model = new ChatOpenAI({
    modelName: "gpt-4-vision-preview",
    maxTokens: 1000,
  });
 
  /**
   * Chat models stream message chunks rather than bytes, so this
   * output parser handles serialization and encoding.
   */
  const outputParser = new BytesOutputParser();
 
  /*
   * Can also initialize as:
   *
   * import { RunnableSequence } from "langchain/schema/runnable";
   * const chain = RunnableSequence.from([prompt, model, outputParser]);
   */
  const chain = prompt.pipe(model).pipe(outputParser);
 
  const stream = await chain.stream({
    chat_history: formattedPreviousMessages.join('\n'),
    input: currentMessageContent,
  });
 
  return new StreamingTextResponse(stream);
}