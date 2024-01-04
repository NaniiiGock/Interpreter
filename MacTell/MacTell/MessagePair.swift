//
//  MessagePair.swift
//  MacTell
//
//  Created by Yaroslav Korch on 04.01.2024.
//

import SwiftUI

enum StatusCode: Int {
    // internal codes
    case noActionTaken = -1     // yet to be sent
    
    // external (API) codes
    case sentForExecution = 0          // no confirmation + is safe
    case userConfirmationNeeded = 1    // needs confirmation + maybe not safe
    case serverCrash = 7               // CriticalError
    case executedSuccessfully = 10     // The execution was successful
    case executionError = 11           // The execution was unsuccessful
}

struct MessagePair: Identifiable {
    let id = UUID()
    let userInput: String
    var llmResponse: LocalizedStringKey = ""
    var isSaved: Bool = false
    var statusCode: StatusCode = StatusCode.noActionTaken
    
    mutating func receiveLLMResponse(llmResponse: LocalizedStringKey, statusCode: StatusCode) {
        self.llmResponse = llmResponse
        self.statusCode = statusCode
    }
    
    mutating func toggle_bookmark() {
        self.isSaved = !self.isSaved
    }
}


struct MessageView: View {
    @Binding var messagePair: MessagePair
    
    let onBookmark: () -> Void

    
    var body: some View {
        HStack(alignment: .firstTextBaseline, spacing: 10) {
            
            VStack(alignment: .leading, spacing: 5) {
                Text(messagePair.userInput)
                Text(messagePair.llmResponse)
                    .foregroundColor(.purple)
                Spacer()
                
            }
            Spacer()

            VStack(alignment: .trailing, spacing: 5) {
                HStack {
                    Button(action: onBookmark) {
                        Image(systemName: messagePair.isSaved ? "bookmark.fill" : "bookmark")
                    }
                    
                    Button(action: rerunMe) {
                        Image(systemName: messagePair.statusCode == StatusCode.userConfirmationNeeded ? "checkmark" : "arrow.clockwise")
                    }
                }
               
                Spacer()

                HStack {
                    statusIcon
                    
                    Text(statusText)
                        .foregroundColor(statusColor)
                }
            }
        }
        .padding()
        .background(Color.gray.opacity(0.2))
        .cornerRadius(10)
        .padding()
    }
    
    func rerunMe(){
        // TODO: integrate Python
        messagePair.statusCode = StatusCode.sentForExecution
    }
    
    
    private var statusIcon: Image {
        switch messagePair.statusCode {
        case .noActionTaken, .sentForExecution:
            return Image(systemName: "hourglass")
        case .userConfirmationNeeded:
            return Image(systemName: "exclamationmark.circle")
        case .serverCrash:
            return Image(systemName: "xmark.octagon")
        case .executedSuccessfully:
            return Image(systemName: "checkmark.circle")
        case .executionError:
            return Image(systemName: "exclamationmark.triangle")
        }
    }

    private var statusText: String {
        switch messagePair.statusCode {
        case .noActionTaken, .sentForExecution:
            return "Waiting for Completion"
        case .userConfirmationNeeded:
            return "Confirmation Needed"
        case .serverCrash:
            return "Server Error"
        case .executedSuccessfully:
            return "Executed Successfully"
        case .executionError:
            return "Execution Error"
        }
    }

    private var statusColor: Color {
        switch messagePair.statusCode {
        case .noActionTaken, .sentForExecution:
            return Color.gray
        case .userConfirmationNeeded:
            return Color.yellow
        case .serverCrash:
            return Color.red
        case .executedSuccessfully:
            return Color.green
        case .executionError:
            return Color.orange
        }
    }

}


struct MessageView_Previews: PreviewProvider {
    struct PreviewWrapper: View {
        @State var sampleMessagePair = MessagePair(userInput: "Sample input", llmResponse: "Some LLM Response")

        var body: some View {
            MessageView(messagePair: $sampleMessagePair, onBookmark: {sampleMessagePair.toggle_bookmark()})
        }
    }

    static var previews: some View {
        PreviewWrapper()
    }
}

