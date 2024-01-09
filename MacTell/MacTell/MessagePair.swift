//
//  MessagePair.swift
//  MacTell
//
//  Created by Yaroslav Korch on 04.01.2024.
//

import Foundation
import SwiftUI

enum StatusCode: Int, Codable {
    case noActionTaken = -1 // default

    case sentForExecution = 0 // command's execution has started.
    case askConfirmation = 1 // app has to ask user for execution confirmation.

    case requestSentToAPI = 2 // app’s UserRequest has been submitted to LLM.

    case submitUserResponse = 3 // The app asks server to submit userInput to LLM.
    case askRerun = 4 // User wants to rerun the command.

    case serverCrash = 7 // CriticalError
    case executedSuccessfully = 10 // The execution was successful
    case executionError = 11 // The execution was unsuccessful

    case saveToBookmarks = 15
    case removeFromBookmarks = 16
    // TODO: add garbage bin button
    case deleteUserMessage = 18
    case askAllSaved = 19
    case sendAllSaved = 20
}

func getFormattedDate(date: Date) -> String {
    let formatter = DateFormatter()
    formatter.dateStyle = .short
    formatter.timeStyle = .short
    return formatter.string(from: date)
}

class MessagePair: Identifiable, ObservableObject {
    let id: UUID
    let userInput: String
    @Published var llmResponse: LocalizedStringKey
    @Published var isSaved: Bool
    @Published var statusCode: StatusCode
    let date: String

    init(id: UUID = UUID(),
         userInput: String = "",
         llmResponse: LocalizedStringKey = "",
         isSaved: Bool = false,
         statusCode: StatusCode = .noActionTaken,
         date: String = getFormattedDate(date: Date()))
    {
        self.id = id
        self.userInput = userInput
        self.llmResponse = llmResponse
        self.isSaved = isSaved
        self.statusCode = statusCode
        self.date = date
    }

    func buildJSONAndSendToServer(statusCode: StatusCode, modifyStatus: Bool) {
        var userServerInteractionData = UserServerInteractionDataBuilder().build_all(messagePair: self)
        userServerInteractionData.statusCode = statusCode

        WebSocketManager.shared.sendMessage(userServerInteractionData)

        if modifyStatus {
            self.statusCode = statusCode
        }
    }

    func sendInputTextToLLM() {
        self.buildJSONAndSendToServer(statusCode: .submitUserResponse, modifyStatus: true)
    }

    func toggleBookmark() {
        self.buildJSONAndSendToServer(statusCode: self.isSaved ? .removeFromBookmarks : .saveToBookmarks, modifyStatus: false)
        self.isSaved.toggle()
    }

    func addToBookmarks() {
        assert(!self.isSaved)
        self.toggleBookmark()
    }

    func rerunMe() {
        self.buildJSONAndSendToServer(statusCode: .askRerun, modifyStatus: true)
    }

    func processReceivedData(userServerInteractionData: UserServerInteractionData) {
        self.statusCode = userServerInteractionData.statusCode

        switch userServerInteractionData.statusCode {
        case .sentForExecution, .askConfirmation:
            self.llmResponse = LocalizedStringKey(userServerInteractionData.llmResponse)
        case .requestSentToAPI, .serverCrash:
            return
        case .executedSuccessfully, .executionError:
            _ = userServerInteractionData.StdOut
            _ = userServerInteractionData.StdErr
        // TODO: change the view to show the stdout and stderr
        default:
            print("ERROR: MessagePair does not support such Status Code:", userServerInteractionData.statusCode)
        }
    }
}

struct StatusAppearance {
    var icon: Image
    var text: String
    var color: Color
}

extension MessagePair {
    func getStatusAppearance() -> StatusAppearance {
        // TODO: change the texts
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
        ]

        return appearance[self.statusCode] ?? .init(icon: Image(systemName: "questionmark"), text: "Unknown Status", color: .black)
    }
}

struct MessageView: View {
    @ObservedObject var messagePair: MessagePair

    var body: some View {
        HStack(alignment: .firstTextBaseline, spacing: 10) {
            VStack(alignment: .leading, spacing: 5) {
                Text(self.messagePair.userInput)
                Text(self.messagePair.llmResponse)
                    .foregroundColor(.purple)
                Spacer()
                Text(self.messagePair.date)
                    .font(.system(size: 10))
                    .foregroundColor(.gray)
            }
            Spacer()

            VStack(alignment: .trailing, spacing: 5) {
                HStack {
                    Button(action: { self.messagePair.toggleBookmark() }) {
                        Image(systemName: self.messagePair.isSaved ? "bookmark.fill" : "bookmark")
                    }

                    Button(action: { self.messagePair.rerunMe() }) {
                        Image(systemName: self.messagePair.statusCode == StatusCode.askConfirmation ? "checkmark" : "arrow.clockwise")
                    }
                }

                Spacer()

                HStack {
                    let statusAppearance = self.messagePair.getStatusAppearance()

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
            MessageView(messagePair: self.sampleMessagePair)
        }
    }

    static var previews: some View {
        PreviewWrapper()
    }
}
