//
//  MessagePair.swift
//  MacTell
//
//  Created by Yaroslav Korch on 04.01.2024.
//

import SwiftUI
import Foundation

enum StatusCode: Int, Codable {
    case noActionTaken = -1            // default

    case sentForExecution = 0          // command's execution has started.
    case askConfirmation = 1           // app has to ask user for execution confirmation.
    
    case requestSentToAPI = 2          // app’s UserRequest has been submitted to LLM.
    
    case submitUserResponse = 3        // The app asks server to submit userInput to LLM.
    case askRerun = 4                  // User wants to rerun the command.
    
    case serverCrash = 7               // CriticalError
    case executedSuccessfully = 10     // The execution was successful
    case executionError = 11           // The execution was unsuccessful
    
    case saveToBookmarks = 15
    case removeFromBookmarks = 16
    case deleteAllUnsaved = 17
    case deleteUserMessage = 18
}


struct MessagePair: Identifiable {
    let id = UUID()
    let userInput: String
    var llmResponse: LocalizedStringKey = ""
    var isSaved: Bool = false
    var statusCode: StatusCode = StatusCode.noActionTaken
    let date: Date = Date()
    
    static var webSocketManager = WebSocketManager()
    

    mutating func buildJSONAndSendToServer(statusCode: StatusCode, modifyStatus: Bool) {
        var userServerInteractionData = UserServerInteractionDataBuilder().build_all(messagePair: self)
        userServerInteractionData.statusCode = statusCode

        DispatchQueue.main.async {
            MessagePair.webSocketManager.sendMessage(userServerInteractionData)
        }
        
        if modifyStatus {
            self.statusCode = statusCode
        }
        
        
    }
    
    mutating func sendInputTextToLLM() {
        buildJSONAndSendToServer(statusCode: .submitUserResponse, modifyStatus: true)

        // TODO: integrate Server Response
        // let (llmResponse, responseCode): (LocalizedStringKey, StatusCode) = ("you sure you wanna spend the cents you've worked for?", StatusCode.sentForExecution)
        // self.llmResponse = llmResponse
        // self.statusCode = responseCode
    }
    
    
    mutating func toggleBookmark() {
        buildJSONAndSendToServer(statusCode: self.isSaved ? .removeFromBookmarks : .saveToBookmarks, modifyStatus: false)
        self.isSaved = !self.isSaved
    }

    mutating func addToBookmarks() {
        assert(!self.isSaved)
        toggleBookmark()
    }

    mutating func rerunMe() {
        buildJSONAndSendToServer(statusCode: .askRerun, modifyStatus: true)
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

struct StatusAppearance {
    var icon: Image
    var text: String
    var color: Color
}

extension MessagePair {
    func getStatusAppearance() -> StatusAppearance {
        let appearance: [StatusCode: StatusAppearance] = [
            .noActionTaken: .init(icon: Image(systemName: "ellipsis.circle"), text: "No Action Taken", color: .gray),
            .sentForExecution: .init(icon: Image(systemName: "hourglass"), text: "Sent for Execution", color: .blue),
            .askConfirmation: .init(icon: Image(systemName: "questionmark.circle"), text: "Confirmation Needed", color: .orange),
            .requestSentToAPI: .init(icon: Image(systemName: "paperplane"), text: "Request Sent", color: .green),
            .submitUserResponse: .init(icon: Image(systemName: "text.bubble"), text: "Response Submitted", color: .purple),
            .askRerun: .init(icon: Image(systemName: "arrow.clockwise"), text: "Rerun Requested", color: .yellow),
            .serverCrash: .init(icon: Image(systemName: "exclamationmark.triangle"), text: "Server Error", color: .red),
            .executedSuccessfully: .init(icon: Image(systemName: "checkmark.circle"), text: "Executed Successfully", color: .green),
            .executionError: .init(icon: Image(systemName: "xmark.octagon"), text: "Execution Error", color: .red),
            .saveToBookmarks: .init(icon: Image(systemName: "bookmark.fill"), text: "Saved", color: .blue),
            .removeFromBookmarks: .init(icon: Image(systemName: "bookmark.slash"), text: "Removed", color: .gray),
            .deleteAllUnsaved: .init(icon: Image(systemName: "trash"), text: "All Unsaved Deleted", color: .purple),
            .deleteUserMessage: .init(icon: Image(systemName: "trash.slash"), text: "Message Deleted", color: .purple)
        ]

        return appearance[self.statusCode] ?? .init(icon: Image(systemName: "questionmark"), text: "Unknown Status", color: .black)
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
                    .font(.system(size: 10))
                    .foregroundColor(.gray)

                
            }
            Spacer()

            VStack(alignment: .trailing, spacing: 5) {
                
                HStack {
                    
                    Button(action: {self.messagePair.toggleBookmark()}) {
                        Image(systemName: messagePair.isSaved ? "bookmark.fill" : "bookmark")
                    }
                    
                    Button(action: {self.messagePair.rerunMe()}) {
                        Image(systemName: messagePair.statusCode == StatusCode.askConfirmation ? "checkmark" : "arrow.clockwise")
                    }
                }
               
                Spacer()

                HStack {
                    let statusAppearance = messagePair.getStatusAppearance()

                    statusAppearance.icon
                    Text(statusAppearance.text)
                        .foregroundColor(statusAppearance.color)
                }
                
            }
        }
        .padding()
        .background(Color.gray.opacity(0.2))
        .cornerRadius(10)
        .padding()
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
