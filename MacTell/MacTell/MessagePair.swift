//
//  MessagePair.swift
//  MacTell
//
//  Created by Yaroslav Korch on 04.01.2024.
//

import SwiftUI
import Foundation

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
    let date: Date = Date()
    

    mutating func sendInputTextToLLM() {
        // TODO: integrate Python
        let (llmResponse, responseCode): (LocalizedStringKey, StatusCode) = ("you sure you wanna spend the cents you've worked for?", StatusCode.sentForExecution)
        
        self.llmResponse = llmResponse
        self.statusCode = responseCode
        
    }
    
    mutating func addToBookmarks() {
        // TODO: integrate Python
        self.isSaved = !self.isSaved
    }

    mutating func toggleBookmark() {
        // TODO: integrate Python
        self.isSaved = !self.isSaved
    }
    
    mutating func rerunMe() {
        // TODO: integrate Python
        self.statusCode = StatusCode.sentForExecution
    }
}

extension MessagePair {
    var formattedDate: String {
        let formatter = DateFormatter()
        formatter.dateStyle = .short
        formatter.timeStyle = .short
        return formatter.string(from: date)
    }
}



struct MessageView: View {
    @Binding var messagePair: MessagePair
    
    var body: some View {
        HStack(alignment: .firstTextBaseline, spacing: 10) {
            
            VStack(alignment: .leading, spacing: 5) {
                Text(messagePair.userInput)
                Text(messagePair.llmResponse)
                    .foregroundColor(.purple)
                Spacer()
                Text(messagePair.formattedDate)
                    .font(.system(size: 10))  // Adjust font size as needed
                    .foregroundColor(.gray)

                
            }
            Spacer()

            VStack(alignment: .trailing, spacing: 5) {
                
                HStack {
                    
                    Button(action: {self.messagePair.toggleBookmark()}) {
                        Image(systemName: messagePair.isSaved ? "bookmark.fill" : "bookmark")
                    }
                    
                    Button(action: {self.messagePair.rerunMe()}) {
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
            MessageView(messagePair: $sampleMessagePair)
        }
    }

    static var previews: some View {
        PreviewWrapper()
    }
}
